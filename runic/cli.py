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
        # Get kebab-case directory name
        track_dir_name = memory_manager._get_track_dir_name(name)
        # Get Title Case display name
        display_name = memory_manager._to_title_case(name)
        
        click.echo(f"Track '{display_name}' created successfully!")
        click.echo(f"Edit the track files at:")
        click.echo(f"  .runic/memory/tracks/{track_dir_name}/active-context.md")
        click.echo(f"  .runic/memory/tracks/{track_dir_name}/progress.md")
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
        # Convert track name to kebab-case for directory path
        track_dir_name = memory_manager._get_track_dir_name(track)
        track_dir = os.path.join('.runic/memory/tracks', track_dir_name)
        
        if not os.path.exists(track_dir):
            click.echo(f"Track '{track}' not found!")
            return
        
        # Get Title Case display name
        display_name = memory_manager._to_title_case(track)
        
        click.echo(f"Updating memory files for track '{display_name}'...")
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

@click.command()
def init():
    """Initialize Runic in the current project"""
    # Create .runic directory if it doesn't exist
    if not os.path.exists('.runic'):
        os.makedirs('.runic')
    
    # Get template directory path (now .runic in the package)
    template_dir = os.path.join(os.path.dirname(__file__), '.runic')
    
    # Create symlinks for all files except memory.templates
    for root, dirs, files in os.walk(template_dir):
        # Skip memory.templates directory for symlinking
        if 'memory.templates' in root:
            continue
            
        # Get the relative path from template_dir
        rel_path = os.path.relpath(root, template_dir)
        
        # Create the corresponding directory in .runic
        if rel_path != '.':
            target_dir = os.path.join('.runic', rel_path)
            os.makedirs(target_dir, exist_ok=True)
        else:
            target_dir = '.runic'
        
        # Create symlinks for all files in the current directory
        for file in files:
            src = os.path.join(root, file)
            dst = os.path.join(target_dir, file)
            
            # Create relative symlink
            rel_src = os.path.relpath(src, os.path.dirname(dst))
            create_symlink(rel_src, dst)
    
    # Copy memory.templates to memory
    memory_template_dir = os.path.join(template_dir, 'memory.templates')
    memory_dir = os.path.join('.runic', 'memory')
    
    if os.path.exists(memory_template_dir):
        # Copy the entire directory
        shutil.copytree(memory_template_dir, memory_dir, dirs_exist_ok=True)
    
    # Create memory directory structure
    memory_manager = MemoryManager()
    memory_manager.ensure_directories()
    
    click.echo("Runic initialized successfully!")
    click.echo("Core files have been symlinked and memory templates have been copied to .runic directory.")

@click.command()
@click.option('--force', is_flag=True, help='Force update of memory files')
def update(force):
    """Update Runic symlinks to point to the latest package files"""
    if not os.path.exists('.runic'):
        click.echo("No .runic directory found. Run 'runic init' first.")
        return
    
    # Get template directory path
    template_dir = os.path.join(os.path.dirname(__file__), '.runic')
    
    # Update symlinks
    updated_links = 0
    for root, dirs, files in os.walk(template_dir):
        # Skip memory.templates directory
        if 'memory.templates' in root:
            continue
            
        # Get the relative path from template_dir
        rel_path = os.path.relpath(root, template_dir)
        
        # Get the corresponding directory in .runic
        if rel_path != '.':
            target_dir = os.path.join('.runic', rel_path)
        else:
            target_dir = '.runic'
        
        # Create the directory if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)
        
        # Update symlinks for all files in the current directory
        for file in files:
            src = os.path.join(root, file)
            dst = os.path.join(target_dir, file)
            
            # If the destination exists and is a symlink, update it
            if os.path.exists(dst):
                if os.path.islink(dst):
                    os.unlink(dst)
                    rel_src = os.path.relpath(src, os.path.dirname(dst))
                    create_symlink(rel_src, dst)
                    updated_links += 1
                elif force:
                    # If force is specified, backup and replace regular files
                    backup = f"{dst}.bak"
                    shutil.copy2(dst, backup)
                    os.unlink(dst)
                    rel_src = os.path.relpath(src, os.path.dirname(dst))
                    create_symlink(rel_src, dst)
                    updated_links += 1
                    click.echo(f"Backed up and replaced {dst} (backup at {backup})")
            else:
                # If the destination doesn't exist, create the symlink
                rel_src = os.path.relpath(src, os.path.dirname(dst))
                create_symlink(rel_src, dst)
                updated_links += 1
    
    click.echo(f"Updated {updated_links} symlinks to point to the latest package files.")
    
    # Optionally update memory files if --force is specified
    if force:
        memory_template_dir = os.path.join(template_dir, 'memory.templates')
        memory_dir = os.path.join('.runic', 'memory')
        
        # Backup memory directory
        backup_dir = f"{memory_dir}.bak.{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        shutil.copytree(memory_dir, backup_dir)
        click.echo(f"Backed up memory directory to {backup_dir}")
        
        # Copy new templates, preserving existing files
        for root, dirs, files in os.walk(memory_template_dir):
            rel_path = os.path.relpath(root, memory_template_dir)
            target_dir = os.path.join(memory_dir, rel_path) if rel_path != '.' else memory_dir
            os.makedirs(target_dir, exist_ok=True)
            
            for file in files:
                src = os.path.join(root, file)
                dst = os.path.join(target_dir, file)
                
                # Only copy if the file doesn't exist or is newer
                if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
                    shutil.copy2(src, dst)
                    click.echo(f"Updated {dst}")
        
        click.echo("Memory files have been updated. Previous versions are available in the backup directory.")

@click.command()
def migrate():
    """Migrate an existing .runic directory to use symlinks"""
    if not os.path.exists('.runic'):
        click.echo("No .runic directory found. Run 'runic init' first.")
        return
    
    # Backup existing .runic directory
    backup_dir = f".runic.bak.{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    shutil.copytree('.runic', backup_dir)
    click.echo(f"Backed up .runic directory to {backup_dir}")
    
    # Get template directory path
    template_dir = os.path.join(os.path.dirname(__file__), '.runic')
    
    # Replace core files with symlinks
    for root, dirs, files in os.walk(template_dir):
        # Skip memory.templates directory
        if 'memory.templates' in root:
            continue
            
        # Get the relative path from template_dir
        rel_path = os.path.relpath(root, template_dir)
        
        # Get the corresponding directory in .runic
        if rel_path != '.':
            target_dir = os.path.join('.runic', rel_path)
        else:
            target_dir = '.runic'
        
        # Create the directory if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)
        
        # Replace files with symlinks
        for file in files:
            src = os.path.join(root, file)
            dst = os.path.join(target_dir, file)
            
            # If the destination exists, replace it with a symlink
            if os.path.exists(dst):
                os.unlink(dst)
            
            # Create symlink
            create_symlink(src, dst)
    
    click.echo("Migration complete. Core files have been replaced with symlinks.")
    click.echo(f"Your original .runic directory has been backed up to {backup_dir}")

def create_symlink(src, dst):
    """Create a symlink with platform-specific handling"""
    rel_src = os.path.relpath(src, os.path.dirname(dst))
    
    try:
        # For Windows, we need administrator privileges or developer mode enabled
        if os.name == 'nt':  # Windows
            # Check if running with admin privileges or in developer mode
            try:
                os.symlink(rel_src, dst)
            except OSError:
                # Fall back to copying if symlink creation fails
                shutil.copy2(src, dst)
                click.echo(f"Note: Created copy instead of symlink for {dst} (Windows requires admin privileges or developer mode for symlinks)")
        else:  # Unix-like systems
            os.symlink(rel_src, dst)
    except Exception as e:
        click.echo(f"Warning: Failed to create symlink {dst}: {e}")
        # Fall back to copying
        shutil.copy2(src, dst)

# Register commands
cli.add_command(track)
cli.add_command(mem)
cli.add_command(integrate)
cli.add_command(init)
cli.add_command(update)
cli.add_command(migrate)

if __name__ == '__main__':
    cli()
