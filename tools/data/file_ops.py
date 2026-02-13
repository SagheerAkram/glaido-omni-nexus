"""
Tool: File Operations
Purpose: Deterministic file I/O operations with safety checks
Category: data
Created: 2026-02-13T21:05:00+05:00
"""

import sys
import json
from pathlib import Path
from typing import Any, Optional, Dict, List
import shutil

# Add utilities to path
sys.path.append(str(Path(__file__).parent.parent / "utilities"))
from logger import info, error, warning


def read_json(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Safely read JSON file.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Parsed JSON data or None on error
    """
    if not file_path.exists():
        error(f"File not found: {file_path}", service="data")
        return None
    
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
        info(f"Read JSON from {file_path.name}", service="data")
        return data
    except json.JSONDecodeError as e:
        error(f"Invalid JSON in {file_path}: {e}", service="data")
        return None


def write_json(file_path: Path, data: Dict[str, Any], indent: int = 2) -> bool:
    """
    Safely write JSON file with atomic operation.
    
    Args:
        file_path: Path to JSON file
        data: Data to write
        indent: JSON indentation
        
    Returns:
        True if successful
    """
    temp_path = file_path.with_suffix('.tmp')
    
    try:
        # Write to temp file
        temp_path.write_text(
            json.dumps(data, indent=indent),
            encoding="utf-8"
        )
        
        # Validate it's valid JSON
        json.loads(temp_path.read_text(encoding="utf-8"))
        
        # Atomic move
        shutil.move(str(temp_path), str(file_path))
        
        info(f"Wrote JSON to {file_path.name}", service="data")
        return True
        
    except Exception as e:
        error(f"Failed to write JSON to {file_path}: {e}", service="data")
        if temp_path.exists():
            temp_path.unlink()
        return False


def read_text(file_path: Path) -> Optional[str]:
    """
    Read text file.
    
    Args:
        file_path: Path to text file
        
    Returns:
        File contents or None on error
    """
    if not file_path.exists():
        error(f"File not found: {file_path}", service="data")
        return None
    
    try:
        content = file_path.read_text(encoding="utf-8")
        info(f"Read text from {file_path.name}", service="data")
        return content
    except Exception as e:
        error(f"Failed to read {file_path}: {e}", service="data")
        return None


def write_text(file_path: Path, content: str) -> bool:
    """
    Write text file with parent directory creation.
    
    Args:
        file_path: Path to text file
        content: Content to write
        
    Returns:
        True if successful
    """
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        info(f"Wrote text to {file_path.name}", service="data")
        return True
    except Exception as e:
        error(f"Failed to write to {file_path}: {e}", service="data")
        return False


def ensure_directory(dir_path: Path) -> bool:
    """
    Ensure directory exists, create if needed.
    
    Args:
        dir_path: Directory path
        
    Returns:
        True if directory exists or was created
    """
    try:
        dir_path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        error(f"Failed to create directory {dir_path}: {e}", service="data")
        return False


def list_files(dir_path: Path, pattern: str = "*") -> List[Path]:
    """
    List files in directory matching pattern.
    
    Args:
        dir_path: Directory to search
        pattern: Glob pattern
        
    Returns:
        List of matching file paths
    """
    if not dir_path.exists():
        warning(f"Directory not found: {dir_path}", service="data")
        return []
    
    try:
        files = list(dir_path.glob(pattern))
        info(f"Found {len(files)} files matching '{pattern}' in {dir_path.name}", service="data")
        return files
    except Exception as e:
        error(f"Failed to list files in {dir_path}: {e}", service="data")
        return []


def safe_delete(file_path: Path, backup: bool = True) -> bool:
    """
    Safely delete file with optional backup.
    
    Args:
        file_path: File to delete
        backup: Create .bak backup before deletion
        
    Returns:
        True if successful
    """
    if not file_path.exists():
        warning(f"File not found for deletion: {file_path}", service="data")
        return False
    
    try:
        if backup:
            backup_path = file_path.with_suffix(file_path.suffix + '.bak')
            shutil.copy2(str(file_path), str(backup_path))
            info(f"Created backup: {backup_path.name}", service="data")
        
        file_path.unlink()
        info(f"Deleted file: {file_path.name}", service="data")
        return True
        
    except Exception as e:
        error(f"Failed to delete {file_path}: {e}", service="data")
        return False


if __name__ == "__main__":
    # CLI testing
    if len(sys.argv) < 2:
        print("Usage: python file_ops.py <command> [args]")
        print("Commands:")
        print("  read-json <file>")
        print("  write-json <file> '<json_data>'")
        print("  read-text <file>")
        print("  list <directory> [pattern]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "read-json" and len(sys.argv) > 2:
        data = read_json(Path(sys.argv[2]))
        if data:
            print(json.dumps(data, indent=2))
    
    elif command == "write-json" and len(sys.argv) > 3:
        file_path = Path(sys.argv[2])
        json_data = json.loads(sys.argv[3])
        write_json(file_path, json_data)
    
    elif command == "read-text" and len(sys.argv) > 2:
        content = read_text(Path(sys.argv[2]))
        if content:
            print(content)
    
    elif command == "list" and len(sys.argv) > 2:
        pattern = sys.argv[3] if len(sys.argv) > 3 else "*"
        files = list_files(Path(sys.argv[2]), pattern)
        for file in files:
            print(file)
    
    else:
        error("Invalid command or missing arguments")
        sys.exit(1)
