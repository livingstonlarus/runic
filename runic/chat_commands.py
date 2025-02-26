"""
Chat commands module for Runic.

This module provides functions for handling chat commands in the Runic framework.
It focuses on commands that AI agents can use within the chat interface.
"""

import git
import os
import datetime
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any, Union

def handle_branch_command(subcommand: str, args: List[str]) -> str:
    """
    Handle branch management commands.
    
    Args:
        subcommand: The branch subcommand (create, delete, merge, list, update, ready)
        args: Arguments for the subcommand
        
    Returns:
        A string response to be displayed in the chat
    """
    if not subcommand:
        return "Error: Branch subcommand is required. Available commands: create, delete, merge, list, update, ready"
    
    try:
        if subcommand == 'create':
            return handle_branch_create(args)
        elif subcommand == 'delete':
            return handle_branch_delete(args)
        elif subcommand == 'merge':
            return handle_branch_merge(args)
        elif subcommand == 'list':
            return handle_branch_list(args)
        elif subcommand == 'update':
            return handle_branch_update(args)
        elif subcommand == 'ready':
            return handle_branch_ready(args)
        else:
            return f"Unknown branch command: {subcommand}. Available commands: create, delete, merge, list, update, ready"
    except git.GitCommandError as e:
        return f"Git error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def handle_branch_create(args: List[str]) -> str:
    """
    Create a new Git branch with track prefix.
    
    Note: This command behaves differently for Orchestrator vs Specialist agents:
    - Orchestrator: Can create branches for any track
    - Specialist: Should create branches prefixed with their track name
    
    Args:
        args: Command arguments [branch_name]
        
    Returns:
        Success or error message
    """
    if not args:
        return "Error: Branch name is required. Usage: $branch create <name>"
    
    branch_name = args[0]
    
    # Note: The agent should prefix the branch name with the track name if it's a specialist
    
    try:
        repo = git.Repo('.')
        repo.git.checkout('-b', branch_name)
        return f"Branch '{branch_name}' created successfully."
    except git.GitCommandError as e:
        return f"Git error: {str(e)}"

def handle_branch_delete(args: List[str]) -> str:
    """
    Delete a Git branch.
    
    Note: This command behaves differently for Orchestrator vs Specialist agents:
    - Orchestrator: Can delete branches for any track
    - Specialist: Should only delete branches for their track
    
    Args:
        args: Command arguments [branch_name]
        
    Returns:
        Success or error message
    """
    if not args:
        return "Error: Branch name is required. Usage: $branch delete <name>"
    
    branch_name = args[0]
    
    # Note: The agent should verify the branch belongs to its track if it's a specialist
    
    try:
        repo = git.Repo('.')
        repo.git.branch('-d', branch_name)
        return f"Branch '{branch_name}' deleted successfully."
    except git.GitCommandError as e:
        return f"Git error: {str(e)}"

def handle_branch_merge(args: List[str]) -> str:
    """
    Merge a Git branch into main.
    
    Note: This command should only be used by the Orchestrator agent.
    
    Args:
        args: Command arguments [branch_name]
        
    Returns:
        Success or error message
    """
    if not args:
        return "Error: Branch name is required. Usage: $branch merge <name>"
    
    branch_name = args[0]
    
    # Note: The agent should verify it's the Orchestrator before using this command
    
    try:
        repo = git.Repo('.')
        main_branch = 'main' if 'main' in [b.name for b in repo.branches] else 'master'
        
        # Checkout main branch
        repo.git.checkout(main_branch)
        
        # Merge the specified branch
        repo.git.merge(branch_name)
        
        return f"Branch '{branch_name}' merged successfully into '{main_branch}'."
    except git.GitCommandError as e:
        return f"Git error: {str(e)}"

def handle_branch_list(args: List[str]) -> str:
    """
    List Git branches.
    
    Note: This command behaves differently for Orchestrator vs Specialist agents:
    - Orchestrator: Lists all branches grouped by track
    - Specialist: Should filter results to show only branches for their track
    
    Args:
        args: Command arguments (unused)
        
    Returns:
        Formatted list of branches
    """
    try:
        repo = git.Repo('.')
        branches = [b.name for b in repo.branches]
        
        # Group branches by track
        tracks = {}
        for branch in branches:
            parts = branch.split('-', 1)
            if len(parts) > 1 and parts[0] != 'main' and parts[0] != 'master':
                track = parts[0]
                if track not in tracks:
                    tracks[track] = []
                tracks[track].append(branch)
            else:
                if 'other' not in tracks:
                    tracks['other'] = []
                tracks['other'].append(branch)
        
        # Format the output
        result = "Branches by track:\n"
        for track, track_branches in sorted(tracks.items()):
            result += f"\n{track.capitalize()}:\n"
            for branch in sorted(track_branches):
                result += f"- {branch}\n"
        
        return result.strip()
    except git.GitCommandError as e:
        return f"Git error: {str(e)}"

def handle_branch_update(args: List[str]) -> str:
    """
    Update feature branch with latest changes from main.
    
    Note: This command behaves differently for Orchestrator vs Specialist agents:
    - Orchestrator: Can update any branch
    - Specialist: Should only update branches for their track
    
    Args:
        args: Command arguments (unused)
        
    Returns:
        Success or error message
    """
    try:
        repo = git.Repo('.')
        current_branch = repo.active_branch.name
        
        # Ensure we're on a feature branch
        main_branch = 'main' if 'main' in [b.name for b in repo.branches] else 'master'
        if current_branch == main_branch:
            return f"Error: Cannot update {main_branch} branch. Please checkout a feature branch first."
        
        # Note: The agent should verify the branch belongs to its track if it's a specialist
        
        # Update the branch
        repo.git.checkout(main_branch)
        repo.git.pull('origin', main_branch)
        repo.git.checkout(current_branch)
        repo.git.rebase(main_branch)
        
        return f"Branch '{current_branch}' updated with latest changes from '{main_branch}'."
    except git.GitCommandError as e:
        return f"Git error: {str(e)}"

def handle_branch_ready(args: List[str]) -> str:
    """
    Signal that a branch is ready to be merged into main.
    
    Note: This command behaves differently for Orchestrator vs Specialist agents:
    - Orchestrator: Can mark any branch as ready
    - Specialist: Should only mark branches for their track as ready
    
    Args:
        args: Command arguments [branch_name]
        
    Returns:
        Success or error message
    """
    if not args:
        return "Error: Branch name is required. Usage: $branch ready <name>"
    
    branch_name = args[0]
    
    # Note: The agent should verify the branch belongs to its track if it's a specialist
    
    try:
        # Create or update a file in .runic/memory/merge-requests
        merge_dir = Path(".runic/memory/merge-requests")
        merge_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a file for this merge request
        merge_file = merge_dir / f"{branch_name}.md"
        with merge_file.open('w') as f:
            f.write(f"# Merge Request: {branch_name}\n\n")
            f.write(f"## Date Requested\n{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Status\nPending\n\n")
            f.write("## Notes\n[Add notes here]\n")
        
        return f"Branch '{branch_name}' marked as ready for merge. The Orchestrator will be notified."
    except Exception as e:
        return f"Error: {str(e)}"

def handle_track_command(subcommand: str, args: List[str]) -> str:
    """
    Handle track management commands.
    
    Args:
        subcommand: The track subcommand (init, status, list, etc.)
        args: Arguments for the subcommand
        
    Returns:
        A string response to be displayed in the chat
    """
    if not subcommand:
        return "Error: Track subcommand is required. Available commands: init, status, list, update, save"
    
    try:
        if subcommand == 'init':
            return handle_track_init(args)
        # Other track commands would be implemented here
        else:
            return f"Unknown track command: {subcommand}. Available commands: init, status, list, update, save"
    except Exception as e:
        return f"Error: {str(e)}"

def handle_track_init(args: List[str]) -> str:
    """
    Initialize a new track and create its first branch.
    
    Note: This command should only be used by the Orchestrator agent.
    
    Args:
        args: Command arguments [track_name]
        
    Returns:
        Success or error message
    """
    if not args:
        return "Error: Track name is required. Usage: $track init <name>"
    
    track_name = args[0]
    
    # Note: The agent should verify it's the Orchestrator before using this command
    
    try:
        # Create the track using the existing CLI command
        import subprocess
        result = subprocess.run(['runic', 'track', 'init', track_name], 
                               capture_output=True, text=True)
        
        if result.returncode != 0:
            return f"Error initializing track: {result.stderr}"
        
        # Get the track directory name
        from runic.memory import MemoryManager
        memory_manager = MemoryManager()
        track_dir_name = memory_manager._get_track_dir_name(track_name)
        
        # Read the progress.md file to find the first task
        progress_path = Path(f".runic/memory/tracks/{track_dir_name}/progress.md")
        first_task = "initial-setup"  # Default branch name
        
        try:
            content = progress_path.read_text()
            # Look for the first task in the "Upcoming Tasks" section
            upcoming_match = content.split("## Upcoming Tasks", 1)
            if len(upcoming_match) > 1:
                tasks = upcoming_match[1].strip().split('\n')
                for task in tasks:
                    if task.strip().startswith('-'):
                        # Extract the task name and convert to kebab-case
                        task_name = task.strip()[1:].strip()
                        first_task = task_name.lower().replace(' ', '-')
                        break
        except Exception:
            # If we can't read the file or find a task, use the default
            pass
        
        # Create the first branch for this track
        branch_name = f"{track_dir_name}-{first_task}"
        repo = git.Repo('.')
        repo.git.checkout('-b', branch_name)
        
        return f"Track '{track_name}' initialized successfully and branch '{branch_name}' created."
    except git.GitCommandError as e:
        return f"Git error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def parse_chat_command(message: str) -> Optional[Tuple[str, str, List[str]]]:
    """
    Parse a chat command from a message.
    
    Args:
        message: The chat message to parse
        
    Returns:
        A tuple of (command_type, subcommand, args) if the message contains a valid command,
        or None if no command is found
    """
    if not message.startswith('$'):
        return None
    
    # Split the message into parts
    parts = message.split()
    if not parts:
        return None
    
    # Extract the command type (e.g., 'branch', 'track', 'mem')
    command_type = parts[0][1:]  # Remove the '$' prefix
    
    if len(parts) > 1:
        subcommand = parts[1]
        args = parts[2:]
    else:
        subcommand = ''
        args = []
    
    return (command_type, subcommand, args)

def handle_chat_command(message: str) -> Optional[str]:
    """
    Handle a chat command.
    
    Args:
        message: The chat message containing the command
        
    Returns:
        A response string if the message contains a valid command,
        or None if no command is found or the command is not recognized
    """
    parsed = parse_chat_command(message)
    if not parsed:
        return None
    
    command_type, subcommand, args = parsed
    
    if command_type == 'branch':
        return handle_branch_command(subcommand, args)
    elif command_type == 'track':
        return handle_track_command(subcommand, args)
    # Future: Add handlers for other command types (mem, etc.)
    
    return None
