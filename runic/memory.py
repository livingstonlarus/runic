"""
Memory management module for Runic.

This module provides functions for managing memory files in the Runic framework.
It focuses on the core functionality of creating, updating, and reading memory files.
"""

import os
import datetime
from pathlib import Path
from typing import List, Dict, Optional, Union

class MemoryManager:
    """Manages memory files for Runic."""
    
    def __init__(self, base_dir: str = '.runic'):
        """Initialize the memory manager.
        
        Args:
            base_dir: The base directory for Runic files.
        """
        self.base_dir = Path(base_dir)
        self.memory_dir = self.base_dir / 'memory'
        self.tracks_dir = self.memory_dir / 'tracks'
    
    def ensure_directories(self) -> None:
        """Ensure that all required directories exist."""
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.tracks_dir.mkdir(parents=True, exist_ok=True)
    
    def get_core_memory_files(self) -> List[Path]:
        """Get a list of core memory files.
        
        Returns:
            A list of paths to core memory files.
        """
        core_files = [
            self.memory_dir / 'project-brief.md',
            self.memory_dir / 'product-context.md',
            self.memory_dir / 'system-patterns.md',
            self.memory_dir / 'tech-context.md',
            self.memory_dir / 'active-context.md',
            self.memory_dir / 'progress.md'
        ]
        return [f for f in core_files if f.exists()]
    
    def _to_kebab_case(self, name: str) -> str:
        """Convert a string to kebab-case.
        
        Args:
            name: The string to convert.
            
        Returns:
            The kebab-case version of the string.
        """
        return name.lower().replace(' ', '-')
    
    def _to_title_case(self, name: str) -> str:
        """Convert a string to Title Case.
        
        Args:
            name: The string to convert.
            
        Returns:
            The Title Case version of the string.
        """
        return ' '.join(word.capitalize() for word in name.split())
    
    def _get_track_dir_name(self, track_name: str) -> str:
        """Get the directory name for a track.
        
        Args:
            track_name: The display name of the track.
            
        Returns:
            The kebab-case directory name for the track.
        """
        return self._to_kebab_case(track_name)
    
    def get_track_memory_files(self, track: Optional[str] = None) -> Dict[str, List[Path]]:
        """Get a dictionary of track memory files.
        
        Args:
            track: The name of a specific track to get files for. If None, get files for all tracks.
            
        Returns:
            A dictionary mapping track names to lists of track memory files.
        """
        result = {}
        
        if not self.tracks_dir.exists():
            return result
        
        if track:
            track_dir = self.tracks_dir / self._get_track_dir_name(track)
            if track_dir.exists() and track_dir.is_dir():
                track_files = [
                    track_dir / 'active-context.md',
                    track_dir / 'progress.md'
                ]
                result[track] = [f for f in track_files if f.exists()]
        else:
            for track_dir in self.tracks_dir.iterdir():
                if track_dir.is_dir():
                    # For existing tracks, we use the directory name as is
                    # but for display, we convert it back to Title Case
                    dir_name = track_dir.name
                    display_name = self._to_title_case(dir_name.replace('-', ' '))
                    track_files = [
                        track_dir / 'active-context.md',
                        track_dir / 'progress.md'
                    ]
                    result[display_name] = [f for f in track_files if f.exists()]
        
        return result
    
    def get_all_memory_files(self) -> Dict[str, List[Path]]:
        """Get all memory files.
        
        Returns:
            A dictionary with 'core' and 'tracks' keys mapping to lists of memory files.
        """
        return {
            'core': self.get_core_memory_files(),
            'tracks': self.get_track_memory_files()
        }
    
    def update_timestamp(self, file_path: Union[str, Path], timestamp: Optional[str] = None) -> bool:
        """Update the timestamp in a memory file.
        
        Args:
            file_path: The path to the memory file.
            timestamp: The timestamp to use. If None, use the current time.
            
        Returns:
            True if the file was updated, False otherwise.
        """
        file_path = Path(file_path)
        if not file_path.exists():
            return False
        
        if timestamp is None:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            content = file_path.read_text()
            
            # Check if file already has a timestamp section
            if "## Last Updated" in content:
                # Update existing timestamp
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith("## Last Updated"):
                        if i + 1 < len(lines):
                            lines[i + 1] = timestamp
                        else:
                            lines.append(timestamp)
                        break
                updated_content = '\n'.join(lines)
            else:
                # Add timestamp at the end
                updated_content = content.rstrip() + f"\n\n## Last Updated\n{timestamp}\n"
            
            file_path.write_text(updated_content)
            return True
        except Exception as e:
            print(f"Error updating timestamp in {file_path}: {e}")
            return False
    
    def update_all_timestamps(self, timestamp: Optional[str] = None) -> Dict[str, int]:
        """Update timestamps in all memory files.
        
        Args:
            timestamp: The timestamp to use. If None, use the current time.
            
        Returns:
            A dictionary with 'core' and 'tracks' keys mapping to the number of files updated.
        """
        if timestamp is None:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        core_updated = 0
        for file_path in self.get_core_memory_files():
            if self.update_timestamp(file_path, timestamp):
                core_updated += 1
        
        tracks_updated = 0
        track_files = self.get_track_memory_files()
        for track_name, files in track_files.items():
            for file_path in files:
                if self.update_timestamp(file_path, timestamp):
                    tracks_updated += 1
        
        return {
            'core': core_updated,
            'tracks': tracks_updated
        }
    
    def update_track_timestamps(self, track: str, timestamp: Optional[str] = None) -> int:
        """Update timestamps in memory files for a specific track.
        
        Args:
            track: The name of the track to update.
            timestamp: The timestamp to use. If None, use the current time.
            
        Returns:
            The number of files updated.
        """
        if timestamp is None:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        updated = 0
        track_files = self.get_track_memory_files(track)
        for track_name, files in track_files.items():
            for file_path in files:
                if self.update_timestamp(file_path, timestamp):
                    updated += 1
        
        return updated
    
    def create_track(self, track_name: str) -> bool:
        """Create a new track with the given name.
        
        Args:
            track_name: The name of the track to create.
            
        Returns:
            True if the track was created, False if it already exists.
        """
        # Convert track name to kebab-case for directory
        track_dir_name = self._get_track_dir_name(track_name)
        # Convert track name to Title Case for display
        display_name = self._to_title_case(track_name)
        
        track_dir = self.tracks_dir / track_dir_name
        if track_dir.exists():
            return False
        
        track_dir.mkdir(parents=True, exist_ok=True)
        
        # Create active-context.md
        active_context_path = track_dir / 'active-context.md'
        with active_context_path.open('w') as f:
            f.write(f"# {display_name} - Active Context\n\n")
            f.write("## Purpose\n[Description of track purpose]\n\n")
            f.write("## Current Focus\n[Description of current focus]\n\n")
            f.write("## Special Identity\n")
            f.write(f"You are a {display_name} Specialist with deep expertise in this domain. ")
            f.write("You excel at implementing solutions in this area, particularly ")
            f.write("using relevant tools and frameworks. You understand the intricacies ")
            f.write("of the challenges in this domain.\n\n")
            f.write("Your knowledge includes:\n")
            f.write("- [Key technology/API] (latest version X.X.X)\n")
            f.write("- [Related pattern/practice]\n")
            f.write("- [Domain-specific concept]\n")
            f.write("- [Important technique]\n")
            f.write("- [Integration knowledge]\n\n")
            f.write(f"When addressing {display_name} implementation, you focus on [key quality attributes] ")
            f.write("to ensure [desired outcome].\n")
        
        # Create progress.md
        progress_path = track_dir / 'progress.md'
        with progress_path.open('w') as f:
            f.write(f"# {display_name} - Progress\n\n")
            f.write("## Overall Status\n[Brief status description]\n\n")
            f.write("## Completed Tasks\n- [None yet]\n\n")
            f.write("## In Progress\n- [Initial setup]\n\n")
            f.write("## Upcoming Tasks\n- [Future task 1]\n- [Future task 2]\n")
        
        return True
    
    def get_track_status(self, track_name: str) -> Optional[str]:
        """Get the status of a track from its progress file.
        
        Args:
            track_name: The name of the track to get the status for.
            
        Returns:
            The status string, or None if the track or its progress file doesn't exist.
        """
        track_dir_name = self._get_track_dir_name(track_name)
        progress_path = self.tracks_dir / track_dir_name / 'progress.md'
        if not progress_path.exists():
            return None
        
        try:
            content = progress_path.read_text()
            status_match = content.split("## Overall Status", 1)
            if len(status_match) > 1:
                status = status_match[1].split("\n", 1)[0].strip()
                return status
        except Exception as e:
            print(f"Error reading track status: {e}")
        
        return None
    
    def get_all_track_statuses(self) -> Dict[str, Optional[str]]:
        """Get the status of all tracks.
        
        Returns:
            A dictionary mapping track names to their status strings.
        """
        result = {}
        
        if not self.tracks_dir.exists():
            return result
        
        for track_dir in self.tracks_dir.iterdir():
            if track_dir.is_dir():
                dir_name = track_dir.name
                display_name = self._to_title_case(dir_name.replace('-', ' '))
                result[display_name] = self.get_track_status(display_name)
        
        return result 
