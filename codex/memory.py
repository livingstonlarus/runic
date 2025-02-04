from pathlib import Path
from datetime import datetime

class Memory:
    def __init__(self):
        self.memory_dir = Path(".codex/memory")
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize memory files
        self.product_context = self.memory_dir / "productContext.md"
        self.active_context = self.memory_dir / "activeContext.md"
        self.system_patterns = self.memory_dir / "systemPatterns.md"
        self.tech_context = self.memory_dir / "techContext.md"
        self.progress = self.memory_dir / "progress.md"
        
        # Create files if they don't exist
        self._initialize_files()
    
    def _initialize_files(self):
        """Initialize memory files with headers if they don't exist"""
        files = {
            self.product_context: "# Product Context\nKey information about the product, its goals, and requirements.\n\n",
            self.active_context: "# Active Context\nCurrent development context and ongoing tasks.\n\n",
            self.system_patterns: "# System Patterns\nRecurring patterns, conventions, and best practices.\n\n",
            self.tech_context: "# Technical Context\nTechnical decisions, architecture, and dependencies.\n\n",
            self.progress: "# Progress Log\nChronological record of development progress and decisions.\n\n"
        }
        
        for file_path, header in files.items():
            if not file_path.exists():
                file_path.write_text(header)
    
    def add_product_context(self, content):
        """Add product-related context"""
        self._append_to_file(self.product_context, content)
    
    def add_active_context(self, content):
        """Add current development context"""
        self._append_to_file(self.active_context, content)
    
    def add_system_pattern(self, content):
        """Add system pattern or convention"""
        self._append_to_file(self.system_patterns, content)
    
    def add_tech_context(self, content):
        """Add technical context or decision"""
        self._append_to_file(self.tech_context, content)
    
    def log_progress(self, content):
        """Log development progress"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = f"## {timestamp}\n{content}\n\n"
        self._append_to_file(self.progress, entry)
    
    def _append_to_file(self, file_path, content):
        """Append content to a memory file"""
        with file_path.open('a') as f:
            f.write(f"{content}\n\n")
    
    def get_context(self, context_type):
        """Retrieve content from a specific context file"""
        context_files = {
            'product': self.product_context,
            'active': self.active_context,
            'patterns': self.system_patterns,
            'tech': self.tech_context,
            'progress': self.progress
        }
        
        file_path = context_files.get(context_type)
        if not file_path:
            raise ValueError(f"Invalid context type: {context_type}")
        
        return file_path.read_text() if file_path.exists() else ""