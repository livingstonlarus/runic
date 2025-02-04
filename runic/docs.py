import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from markdownify import markdownify as md

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
        import os
        return crawl_website(start_url, max_workers)

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
    """Scrape a single page, extract <main> content, convert to Markdown, and return links within the base path."""
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
            soup.find(id='main-content')
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
        return set()

def crawl_website(start_url, max_workers=10):
    """Crawl the website starting from the start_url within its base path."""
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
        return
    
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
                new_links = future.result()
                # Only add unvisited links
                to_visit.update(new_links - visited)
