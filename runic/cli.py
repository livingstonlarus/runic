import click
import shutil
import os
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


cli.add_command(init)
cli.add_command(docs)

if __name__ == "__main__":
    cli()
