import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from markdownify import markdownify as md

# Import for ZIP handling
import zipfile
import io # For in-memory zip file handling
import tempfile # For temporary directory
from pathlib import Path # For Pathlib
import shutil # For moving directories

# Set to track processed URLs globally
processed_urls = set()

class Docs:
    @staticmethod
    def get_page_title(soup):
        return get_page_title(soup)

    @staticmethod
    def save_markdown(url, content, base_title):
        import os
        return save_markdown(url, content, base_title)

    @staticmethod
    def is_within_base_path(base_url, target_url):
        return is_within_base_path(base_url, target_url)

    @staticmethod
    def scrape_page(url, base_url, base_title):
        return scrape_page(url, base_url, base_title)

    @staticmethod
    def crawl_website(start_url, max_workers=10):
        return crawl_website(start_url, max_workers)

def get_github_base_repo_path(github_url):
    """Extract the base repository path from a GitHub URL.
    Handles both 'tree/main' and 'tree/master' branches.
    """
    parsed_url = urlparse(github_url)
    path_parts = parsed_url.path.strip('/').split('/')
    if len(path_parts) >= 3 and path_parts[2] == 'tree': # Ensure it's a /tree/ URL
        base_path_parts = path_parts[:3] # user/repo/tree
        if len(path_parts) >= 4:
            branch_name = path_parts[3] # Get branch name (main, master, etc.)
            base_path_parts.append(branch_name) # Include branch name in base path
        return "/" + "/".join(base_path_parts)
    return None

def get_page_title(soup):
    """Extract the page title from BeautifulSoup object."""
    title_tag = soup.find('title')
    if title_tag:
        # Clean up the title to be used as a directory name
        title = title_tag.string.strip()
        return ''.join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in title)
    return 'Untitled'

def save_markdown(url, content, base_title):
    """Save Markdown content to a file preserving URL path structure."""
    parsed_url = urlparse(url)
    # Preserve the URL path structure
    path_parts = parsed_url.path.strip('/').split('/')
    
    # Handle the case where the URL ends with a file
    if '.' in path_parts[-1]:
        path_parts[-1] = path_parts[-1].rsplit('.', 1)[0]
    
    # If path is empty, use index
    if not path_parts or path_parts == ['']:
        path_parts = ['index']
    
    # Add .md extension to the last part
    path_parts[-1] += '.md'
    
    # Create the full path under .runic/docs/base_title
    docs_dir = os.environ.get('RUNIC_DOCS_DIR', os.path.join('.runic', 'docs'))
    base_dir = os.path.join(docs_dir, base_title)
    full_path = os.path.join(base_dir, *path_parts)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    with open(full_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Saved: {full_path}")
    return base_dir

def is_within_base_path(base_url, target_url):
    """Check if the target URL is within the base path of the base URL."""
    base_parsed = urlparse(base_url)
    # Strip anchor fragment from target URL
    target_url = target_url.split('#')[0]
    target_parsed = urlparse(target_url)
    return (base_parsed.scheme == target_parsed.scheme and
            base_parsed.netloc == target_parsed.netloc and
            target_parsed.path.startswith(base_parsed.path))

def scrape_page(url, base_url, base_title):
    """Scrape a single page, handle markdown files, directory listings, or GitHub ZIP archives."""
    print(f"Debug: Scraping URL: {url}") # Debug: function entry

    if url.endswith(".md"):
        # Fetch raw markdown content for .md files (still using requests for raw markdown)
        raw_url = url.replace("github.com", "raw.githubusercontent.com").replace("/tree/main", "").replace("/blob/main", "")
        print(f"Debug: Fetching raw markdown URL: {raw_url}") # Debug: raw markdown URL
        response = requests.get(raw_url)
        if response.status_code != 200:
            print(f"Failed to fetch raw markdown from {raw_url}, status code: {response.status_code}")
            return None, None, None
        page_title = url.split('/')[-1].replace(".md", "").replace("-", " ").title() # Extract title from filename
        markdown_content = response.text
        print(f"Debug: Fetched markdown content, title: {page_title}, length: {len(markdown_content)}") # Debug: markdown fetched
        return page_title, markdown_content, set() # No links to extract from raw markdown, return empty set

    parsed_url = urlparse(url)
    if parsed_url.netloc == "github.com":
        print("Debug: GitHub URL detected, using ZIP archive method.") # Debug: GitHub URL detected
        try:
            # 1. Create .runic/docs/.tmp directory
            tmp_docs_dir = Path(".runic/docs/.tmp")
            tmp_docs_dir.mkdir(parents=True, exist_ok=True)
            print(f"Debug: Created temporary docs directory: {tmp_docs_dir}") # Debug: tmp dir created

            # 2. Download ZIP archive to .runic/docs/.tmp
            path_parts = parsed_url.path.strip('/').split('/')
            user = path_parts[0]
            repo = path_parts[1]
            zip_url = f"https://github.com/{user}/{repo}/archive/refs/heads/main.zip" # Construct zip URL
            zip_file_path = tmp_docs_dir / "repo.zip" # Path to save zip file
            print(f"Debug: Downloading ZIP archive from: {zip_url} to {zip_file_path}") # Debug: zip_url

            response = requests.get(zip_url, stream=True) # Use stream=True for large files
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            with open(zip_file_path, 'wb') as f: # Save zip file to disk
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Debug: ZIP archive downloaded to: {zip_file_path}") # Debug: zip downloaded

            # 3. Extract ZIP archive to .runic/docs/.tmp
            extracted_path = tmp_docs_dir / "extracted" # Directory to extract to
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extracted_path)
            print(f"Debug: ZIP archive extracted to: {extracted_path}") # Debug: zip extracted

            # Debug: List contents of extracted ZIP
            print("Debug: Contents of extracted ZIP:")
            extracted_zip_contents = list(extracted_path.iterdir())
            for item in extracted_zip_contents:
                print(f"Debug:   - {item}")

            # 4. Construct paths and move target directory
            repo_name = f"{repo}-main" # GitHub zip root directory name
            base_repo_url_path = get_github_base_repo_path(url) # Dynamically get base repo path
            if not base_repo_url_path:
                print(f"Error: Could not extract base repo path from URL: {url}")
                return "Error: Invalid GitHub URL", "", set() # Indicate error
            print(f"Debug: Base repo URL path: {base_repo_url_path}") # Debug: base repo url path

            # Calculate target_path_in_repo using path parts (Refined)
            base_repo_path_parts = get_github_base_repo_path(url).strip('/').split('/') # Get base path parts again
            url_path_parts = parsed_url.path.strip('/').split('/') # Get URL path parts again
            target_path_parts = url_path_parts[len(base_repo_path_parts):] # Get parts after base path
            target_path_in_repo = "/".join(target_path_parts) # Reconstruct target path
            print(f"Debug: Target path in repo: {target_path_in_repo}") # Debug: target path in repo

            # Construct new base title with repo name and target path
            if target_path_in_repo:
                target_folder_name = target_path_in_repo.replace("/", " - ") # Replace slashes with " - " for folder name
                base_title = f"{repo} - {target_folder_name}" # Combine repo name and target folder
            else:
                base_title = repo # Fallback to just repo name if no target path
            print(f"Debug: New base_title for directory: {base_title}") # Debug: new base_title

            # Construct the documentation path within the ZIP based on the target path
            docs_path_in_zip = extracted_path / repo_name / target_path_in_repo
            print(f"Debug: Dynamic documentation path in ZIP: {docs_path_in_zip}") # Debug: dynamic docs path
            final_docs_dir = Path(".runic/docs") / base_title # Use the new base_title for final directory
            print(f"Debug: Source documentation path in ZIP: {docs_path_in_zip}") # Debug: source docs path
            print(f"Debug: Destination final docs directory: {final_docs_dir}") # Debug: final docs dir

            if docs_path_in_zip.is_dir():
                shutil.move(str(docs_path_in_zip), str(final_docs_dir)) # Move directory
                print(f"Debug: Moved documentation from {docs_path_in_zip} to {final_docs_dir}") # Debug: docs moved
            else:
                print(f"Debug: Documentation path not found in ZIP: {docs_path_in_zip}, skipping move.") # Debug: docs path not found

            # For now, indicate success. Crawling and processing will be next.
            return "GitHub ZIP Download, Extract, Move Success", "", set() # Indicate success, return empty set for links

        except requests.RequestException as e:
            print(f"Error downloading ZIP archive: {e}")
        except zipfile.BadZipFile as e:
            print(f"Error extracting ZIP archive: {e}")
        except Exception as e:
            print(f"Error processing ZIP archive: {e}")
        finally:
            # 5. Cleanup .runic/docs/.tmp directory
            if tmp_docs_dir.is_dir():
                shutil.rmtree(tmp_docs_dir) # Delete temporary directory and its contents
                print(f"Debug: Deleted temporary directory: {tmp_docs_dir}") # Debug: tmp dir deleted

    # --- Re-integrate general website scraping logic from runic/docs.old.py ---
    # If not a GitHub URL or ZIP processing failed, use general scraping:
    print("Debug: Using general website scraping for URL:", url) # Debug: General scraping

     # Strip anchor fragment from the URL before processing
    url = url.split('#')[0]

    # Skip if URL has already been processed
    if url in processed_urls:
        return set()
    
    # Mark URL as processed immediately
    processed_urls.add(url)
    print(f"Processing URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        html_content = response.text

        soup = BeautifulSoup(html_content, 'lxml')
        # Try to find the main content using various common selectors
        main_content = (
            soup.find('main') or
            soup.find('article') or
            soup.find(attrs={"role": "main"}) or
            soup.find(class_='content') or
            soup.find(class_='post-content') or
            soup.find(class_='entry-content') or
            soup.find(class_='markdown-body') or
            soup.find(id='content') or
            soup.find(id='main-content') or
            soup.find(class_='api-content')
        )

        if main_content:
            markdown_content = md(str(main_content), escape_asterisks=False, escape_underscores=False)
            save_markdown(url, markdown_content, base_title)
        else:
            print(f"No <main> or <article> content found on {url}, skipping.")

        links = set()
        for a_tag in soup.find_all('a', href=True):
            # Strip anchor fragments when collecting links
            link = urljoin(url, a_tag['href']).split('#')[0]
            if is_within_base_path(base_url, link):
                links.add(link)
        return links
    except requests.RequestException as e:
        print(f"Failed to scrape {url}: {e}")
        return None, None, set()

def crawl_website(start_url, max_workers=10):
    """Crawl the website for documentation starting from the start_url."""
    print(f"Debug: Starting crawl_website with URL: {start_url}") # Debug: crawl_website start
    # Clear the processed URLs set at the start of each crawl
    processed_urls.clear()
    
    # First, get the title from the start page
    try:
        response = requests.get(start_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        base_title = get_page_title(soup)
    except requests.RequestException as e:
        print(f"Failed to fetch start page: {e}")
        return False
    
    # Initialize visited and to_visit sets
    visited = set()
    to_visit = {start_url}
    
    def scrape_with_title(url):
        return scrape_page(url, start_url, base_title)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while to_visit:
            # Mark URLs as visited before processing
            current_batch = to_visit
            visited.update(current_batch)
            to_visit = set()
            
            futures = {executor.submit(scrape_with_title, url): url for url in current_batch}
            for future in as_completed(futures):
                try:
                    new_links = future.result()
                    # Only add unvisited links
                    to_visit.update(new_links - visited)
                except Exception as e: # Catch exceptions during scraping
                    url_from_future = futures[future]
                    print(f"Error during scraping of {url_from_future}: {e}")
    return True # Indicate success if crawl_website completes without raising unhandled exceptions

def write_markdown_file(output_dir, base_title, page_title, markdown_content):
    """Write the markdown content to a file in the output directory."""
    if not markdown_content.strip(): # Skip empty files
        print(f"Skipping empty content for page: {page_title}")
        return

    file_name = f"{page_title.replace(' ', '_').replace('/', '_')}.md"
    file_path = os.path.join(output_dir, file_name)

    print(f"Debug: Writing markdown file to: {file_path}")

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(markdown_content)
        print(f"Saved: {file_path}")
    except Exception as e:
        print(f"Failed to save markdown file: {e}")
