import click
import shutil
import os
from pathlib import Path
from codex.docs import Docs
from codex.memory import Memory

@click.group()
def cli():
    """Codex CLI - AI Coding Assistant Toolset"""
    pass

@click.command()
@click.argument('url', required=True)
def docs(url):
    """Fetch documentation from given URL"""
    try:
        # Create output directory in .codex/docs
        docs_dir = Path(".codex/docs")
        docs_dir.mkdir(parents=True, exist_ok=True)
        
        # Set the output directory for spider
        os.environ['CODEX_DOCS_DIR'] = str(docs_dir)
        
        # Crawl and process the documentation
        Docs.crawl_website(url)
    except Exception as e:
        print(f"❌ Failed to fetch documentation from {url}: {str(e)}")

@click.command()
def init():
    """Initialize Codex in the current project"""
    # Get templates directory path from package
    templates_dir = Path(__file__).parent / "templates"
    
    # Create target directory by copying templates
    target_dir = Path(".codex")
    if not target_dir.exists():
        shutil.copytree(templates_dir, target_dir)
        print("✅ Codex initialized in this project. Prompt your AI coding assistant with: 'Follow your instructions in .codex/instruct.md' to begin.")
    else:
        print("⚠️ Codex is already initialized in this project.")


cli.add_command(init)
cli.add_command(docs)

if __name__ == "__main__":
    cli()
