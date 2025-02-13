import click
import shutil
import os
import glob
from pathlib import Path
from runic.docs import Docs
from runic.memory import Memory
import importlib.metadata

@click.group()
@click.version_option(importlib.metadata.version('runic'))
def cli():
    """Runic CLI - LLM Memory & Documentation Enhancement Framework"""
    pass

@click.command()
@click.argument('url', required=True)
def docs(url):
    """Fetch documentation from given URL"""
    try:
        # Create output directory in .runic/docs
        docs_dir = Path(".runic/docs")
        docs_dir.mkdir(parents=True, exist_ok=True)

        # Set the output directory for spider
        os.environ['RUNIC_DOCS_DIR'] = str(docs_dir)

        # Crawl and process the documentation
        Docs.crawl_website(url)
    except Exception as e:
        print(f"❌ Failed to fetch documentation from {url}: {str(e)}")

@click.command()
def init():
    """Initialize Runic in the current project"""
    # Get templates directory path from package
    templates_dir = Path(__file__).parent / "templates"

    # Create target directory by copying templates
    target_dir = Path(".runic")
    if not target_dir.exists():
        shutil.copytree(templates_dir, target_dir)
        print("✅ Runic initialized in this project. Prompt your AI assistant with: 'Follow your instructions in .runic/instruct.md' to begin.")
    else:
        print("⚠️ Runic is already initialized in this project.")


@click.command()
@click.argument('paths', nargs=-1, type=click.Path(exists=True))
def concat(paths):
    """Concatenate multiple files and directories into a single markdown file"""
    if not paths:
        print("❌ No paths provided")
        return

    # Create concats directory if it doesn't exist
    concats_dir = Path(".runic/concats")
    concats_dir.mkdir(parents=True, exist_ok=True)

    # Find the next available file number
    existing_files = glob.glob(str(concats_dir / "concat*.md"))
    next_num = 1
    if existing_files:
        numbers = [int(Path(f).stem.replace('concat', '')) for f in existing_files]
        next_num = max(numbers) + 1

    # Create the output file path with padded number
    output_file = concats_dir / f"concat{str(next_num).zfill(3)}.md"

    # Function to collect all files recursively
    def collect_files(path):
        path = Path(path)
        if path.is_file():
            return [path] if path.name != '.DS_Store' else []
        elif path.is_dir():
            files = []
            for item in path.rglob('*'):
                # Skip __pycache__ directories and their contents
                if '__pycache__' in item.parts:
                    continue
                if item.is_file() and item.name != '.DS_Store':
                    files.append(item)
            return sorted(files)
        return []

    # Collect all files from provided paths
    all_files = []
    for path in paths:
        all_files.extend(collect_files(path))

    if not all_files:
        print("❌ No files found in the provided paths")
        return

    # Generate the content
    content = ["# Concatenation of files and directories"]

    # Add path list with hierarchy
    content.append("## Source Paths:")
    for path in paths:
        path = Path(path)
        if path.is_dir():
            content.append(f"- 📁 {path} (directory)")
        else:
            content.append(f"- 📄 {path} (file)")
    content.append("")

    # Add file list
    content.append("## Included Files:")
    for file_path in all_files:
        content.append(f"- {file_path}")
    content.append("")

    # Add each file's content
    content.append("## Contents:")
    for file_path in all_files:
        content.append(f"### {file_path}")
        # Map file extensions to code block languages
        ext_to_lang = {
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.py': 'python',
            '.java': 'java',
            '.c': 'c',
            '.cpp': 'cpp',
            '.cs': 'csharp',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.m': 'objective-c',
            '.h': 'c',
            '.sh': 'bash',
            '.bash': 'bash',
            '.zsh': 'bash',
            '.fish': 'fish',
            '.sql': 'sql',
            '.html': 'html',
            '.xml': 'xml',
            '.css': 'css',
            '.scss': 'scss',
            '.less': 'less',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.md': 'markdown',
            '.r': 'r',
            '.dart': 'dart',
            '.lua': 'lua',
            '.pl': 'perl',
            '.groovy': 'groovy',
            '.dockerfile': 'dockerfile',
            '.vue': 'vue',
            '.elm': 'elm',
            '.ex': 'elixir',
            '.exs': 'elixir',
            '.erl': 'erlang',
            '.fs': 'fsharp',
            '.fsx': 'fsharp',
            '.hs': 'haskell',
            '.lhs': 'haskell'
        }

        # Get file extension and corresponding language
        ext = Path(file_path).suffix.lower()
        lang = ext_to_lang.get(ext, 'plaintext')

        content.append(f"```{lang}")
        try:
            with open(file_path, 'r') as f:
                content.append(f.read().rstrip())
        except Exception as e:
            content.append(f"Error reading file: {str(e)}")
        content.append("```\n")

    # Write the concatenated content
    try:
        with open(output_file, 'w') as f:
            f.write('\n'.join(content))
        print(f"✅ Files concatenated successfully to {output_file}")
    except Exception as e:
        print(f"❌ Failed to write concatenated file: {str(e)}")

@click.command()
@click.argument('path', required=False, type=click.Path(exists=True))
def tree(path):
    """Generate a visual tree structure of the project or specified directory"""
    # Create trees directory if it doesn't exist
    trees_dir = Path(".runic/trees")
    trees_dir.mkdir(parents=True, exist_ok=True)

    # Find the next available file number
    existing_files = glob.glob(str(trees_dir / "tree*.md"))
    next_num = 1
    if existing_files:
        numbers = [int(Path(f).stem.split('-')[0].replace('tree', '')) for f in existing_files]
        next_num = max(numbers) + 1

    # Determine the root directory and create the output filename
    root_dir = Path(path) if path else Path('.')
    file_suffix = ''
    title = '# Current project file structure'

    if path:
        # Create a sanitized version of the path for the filename
        sanitized_path = str(root_dir).lstrip('./').replace('/', '-')
        file_suffix = f'-{sanitized_path}'
        title = f'# File structure of {root_dir}'

    # Create the output file path with padded number and optional path suffix
    output_file = trees_dir / f"tree{str(next_num).zfill(3)}{file_suffix}.md"

    def get_tree(directory, prefix='', is_last=False, exclude_dirs=None):
        if exclude_dirs is None:
            exclude_dirs = set()

        # Get all entries in the directory
        entries = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        entries = [e for e in entries if e.name not in exclude_dirs and not e.name.startswith('.') and e.name != '.DS_Store']

        tree_lines = []
        for i, entry in enumerate(entries):
            is_last_entry = i == len(entries) - 1
            current_prefix = prefix + ('└── ' if is_last_entry else '├── ')
            tree_lines.append(current_prefix + entry.name + ('/' if entry.is_dir() else ''))

            if entry.is_dir():
                # Add vertical line for non-last directories
                next_prefix = prefix + ('    ' if is_last_entry else '│   ')
                tree_lines.extend(get_tree(entry, next_prefix, is_last_entry, exclude_dirs))

        return tree_lines

    try:
        # Generate tree structure excluding .runic and node_modules directories
        tree_lines = [title, '```plaintext']
        tree_lines.extend(get_tree(root_dir, exclude_dirs={'.runic', 'node_modules', '.DS_Store'}))
        tree_lines.append('```')

        # Write the tree structure to file
        with open(output_file, 'w') as f:
            f.write('\n'.join(tree_lines))
        print(f"✅ Project tree structure generated successfully in {output_file}")
    except Exception as e:
        print(f"❌ Failed to generate tree structure: {str(e)}")

cli.add_command(init)
cli.add_command(docs)
cli.add_command(concat)
cli.add_command(tree)

if __name__ == "__main__":
    cli()
