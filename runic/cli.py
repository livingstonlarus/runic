import click
import shutil
import os
from pathlib import Path
import importlib.metadata
from datetime import datetime
from runic.memory import MemoryManager

@click.group()
@click.version_option(importlib.metadata.version('runic'))
def cli():
    """Runic - A framework for parallel development with multiple AI agents"""
    pass

@click.command()
def init():
    """Initialize Runic in the current project"""
    # Create .runic directory if it doesn't exist
    if not os.path.exists('.runic'):
        os.makedirs('.runic')
    
    # Get template directory path
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    
    # Copy all template files to .runic
    for root, dirs, files in os.walk(template_dir):
        # Get the relative path from template_dir
        rel_path = os.path.relpath(root, template_dir)
        
        # Create the corresponding directory in .runic
        if rel_path != '.':
            target_dir = os.path.join('.runic', rel_path)
            os.makedirs(target_dir, exist_ok=True)
        else:
            target_dir = '.runic'
        
        # Copy all files in the current directory
        for file in files:
            src = os.path.join(root, file)
            dst = os.path.join(target_dir, file)
            shutil.copy(src, dst)
    
    # Create memory directory structure
    memory_manager = MemoryManager()
    memory_manager.ensure_directories()
    
    click.echo("Runic initialized successfully!")
    click.echo("All template files have been copied to .runic directory.")

@click.group()
def track():
    """Manage development tracks"""
    pass

@track.command(name="init")
@click.argument('name')
def track_init(name):
    """Create a new track with the given name"""
    memory_manager = MemoryManager()
    memory_manager.ensure_directories()
    
    if memory_manager.create_track(name):
        click.echo(f"Track '{name}' created successfully!")
        click.echo(f"Edit the track files at:")
        click.echo(f"  .runic/memory/tracks/{name}/active-context.md")
        click.echo(f"  .runic/memory/tracks/{name}/progress.md")
    else:
        click.echo(f"Track '{name}' already exists!")

@track.command(name="list")
def track_list():
    """List all tracks"""
    memory_manager = MemoryManager()
    track_files = memory_manager.get_track_memory_files()
    
    if not track_files:
        click.echo("No tracks found. Create one with 'runic track init <name>'")
        return
    
    click.echo("Available tracks:")
    for track in sorted(track_files.keys()):
        click.echo(f"  - {track}")

@track.command(name="status")
def track_status():
    """Show status of all tracks"""
    memory_manager = MemoryManager()
    track_statuses = memory_manager.get_all_track_statuses()
    
    if not track_statuses:
        click.echo("No tracks found. Create one with 'runic track init <name>'")
        return
    
    click.echo("Track Status:")
    for track, status in sorted(track_statuses.items()):
        if status:
            click.echo(f"  - {track}: {status}")
        else:
            click.echo(f"  - {track}: Status not found in progress file")

@click.group()
def mem():
    """Manage memory files"""
    pass

@mem.command(name="update")
@click.option('--track', help='Update only the specified track')
def mem_update(track):
    """Update memory files with timestamps"""
    memory_manager = MemoryManager()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if track:
        track_dir = os.path.join('.runic/memory/tracks', track)
        if not os.path.exists(track_dir):
            click.echo(f"Track '{track}' not found!")
            return
        
        click.echo(f"Updating memory files for track '{track}'...")
        updated = memory_manager.update_track_timestamps(track, timestamp)
        click.echo(f"Updated {updated} files.")
    else:
        click.echo("Updating all memory files...")
        result = memory_manager.update_all_timestamps(timestamp)
        click.echo(f"Updated {result['core']} core files and {result['tracks']} track files.")
    
    click.echo("Memory update complete!")

def update_file_timestamp(file_path, timestamp):
    """Add or update timestamp in a markdown file"""
    memory_manager = MemoryManager()
    return memory_manager.update_timestamp(file_path, timestamp)

@mem.command(name="next")
def mem_next():
    """Determine and execute next steps based on memory analysis"""
    memory_manager = MemoryManager()
    
    click.echo("Analyzing memory files to determine next steps...")
    
    # Get all memory files
    memory_files = memory_manager.get_all_memory_files()
    
    # Check if we have any memory files
    if not memory_files['core'] and not memory_files['tracks']:
        click.echo("No memory files found. Initialize memory files first.")
        return
    
    # Analyze progress.md to find next steps
    progress_file = memory_manager.memory_dir / 'progress.md'
    if progress_file.exists():
        try:
            content = progress_file.read_text()
            # Extract upcoming tasks if available
            upcoming_match = content.split("## Upcoming Tasks", 1)
            if len(upcoming_match) > 1:
                upcoming_tasks = upcoming_match[1].strip()
                if upcoming_tasks:
                    click.echo("Based on memory analysis, recommended next steps:")
                    for line in upcoming_tasks.split('\n'):
                        if line.strip().startswith('-'):
                            click.echo(f"  {line.strip()}")
                else:
                    click.echo("No upcoming tasks found in progress.md.")
            else:
                click.echo("No 'Upcoming Tasks' section found in progress.md.")
        except Exception as e:
            click.echo(f"Error analyzing progress.md: {e}")
    else:
        click.echo("progress.md not found. Create it to track next steps.")
    
    # Check for active tracks
    if memory_files['tracks']:
        click.echo("\nActive tracks:")
        for track_name, files in memory_files['tracks'].items():
            status = memory_manager.get_track_status(track_name)
            click.echo(f"  - {track_name}: {status or 'No status available'}")
    
    click.echo("\nRecommended actions:")
    click.echo("1. Update memory files with recent changes: runic mem update")
    click.echo("2. Review track statuses: runic track status")
    if not memory_files['tracks']:
        click.echo("3. Initialize your first track: runic track init <name>")

@click.group()
def integrate():
    """Integration points for external tools"""
    pass

@integrate.command(name="docs")
@click.argument('url', required=True)
@click.option('--tool', default='crawl4ai', help='Tool to use for documentation fetching (crawl4ai, etc.)')
def integrate_docs(url, tool):
    """Integration point for documentation fetching tools"""
    click.echo(f"Integration point for {tool} to fetch documentation from {url}")
    click.echo("To implement this integration:")
    click.echo(f"1. Install the {tool} package")
    click.echo(f"2. Create an integration script using the example in IMPLEMENTATION.md")
    click.echo(f"3. Call your integration script here with: {url}")
    
    # This is just a placeholder for the integration point
    # In a real implementation, you would import and call the appropriate tool

@integrate.command(name="vector-db")
@click.option('--tool', default='chroma', help='Vector database to use (chroma, faiss, pinecone, etc.)')
@click.option('--action', default='index', help='Action to perform (index, query)')
@click.option('--query', help='Query text for search actions')
def integrate_vector_db(tool, action, query):
    """Integration point for vector database tools"""
    click.echo(f"Integration point for {tool} vector database, action: {action}")
    
    if action == 'index':
        click.echo(f"To implement {tool} indexing:")
        click.echo(f"1. Install the {tool} package")
        click.echo(f"2. Create an indexing script using the example in IMPLEMENTATION.md")
        click.echo(f"3. Call your indexing script here to index memory files")
    elif action == 'query' and query:
        click.echo(f"To implement {tool} querying:")
        click.echo(f"1. Install the {tool} package")
        click.echo(f"2. Create a query script using the example in IMPLEMENTATION.md")
        click.echo(f"3. Call your query script here with: {query}")
    else:
        click.echo("Please specify a valid action and query (for search actions)")

@integrate.command(name="llm")
@click.option('--tool', default='langchain', help='LLM framework to use (langchain, llamaindex, etc.)')
@click.option('--action', required=True, help='Action to perform with the LLM framework')
def integrate_llm(tool, action):
    """Integration point for LLM framework tools"""
    click.echo(f"Integration point for {tool} LLM framework, action: {action}")
    click.echo("To implement this integration:")
    click.echo(f"1. Install the {tool} package")
    click.echo(f"2. Create an integration script using the example in IMPLEMENTATION.md")
    click.echo(f"3. Call your integration script here with action: {action}")


# Register commands
cli.add_command(init)
cli.add_command(track)
cli.add_command(mem)
cli.add_command(integrate)

if __name__ == '__main__':
    cli()
