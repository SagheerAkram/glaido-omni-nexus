#!/usr/bin/env python3
"""
Python Syntax Check Tool
Specialized for Glaido Omni-Nexus

Invariant Compliance:
- Offline-First: Uses standard library 'ast' only.
- Read-Only: Scans files without execution.
- JSON Contract: Emits 'python_syntax' schema.
- Deterministic: Same code -> same result.
"""

import sys
import os
import json
import ast
import time
from pathlib import Path
from datetime import datetime, timezone

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------

TOOL_CATEGORY = "python_syntax"

# Directories to scan relative to workspace root
TARGET_DIRECTORIES = [
    "tools",
    "navigation",
    "cli"
]

# Legacy root scripts to scan explicitly
TARGET_FILES = [
    "architect_enhanced.py"
]

# Files/Dirs to ignore
IGNORE_DIRS = {
    "__pycache__",
    ".git",
    ".tmp",
    "node_modules",
    "venv",
    ".venv"
}

# ------------------------------------------------------------------------------
# Core Logic
# ------------------------------------------------------------------------------

def _get_timestamp():
    """Return ISO 8601 timestamp with timezone"""
    return datetime.now(timezone.utc).astimezone().isoformat()

def get_workspace_root():
    """
    Resolve workspace root.
    Assumes this script is in tools/core/ and root is ../../
    """
    return Path(__file__).resolve().parents[2]

def scan_file(file_path):
    """
    Parse a single file using ast.
    Returns error dict or None.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            ast.parse(content, filename=str(file_path))
            return None
    except SyntaxError as e:
        return {
            "file": str(file_path.relative_to(get_workspace_root())),
            "line": e.lineno,
            "column": e.offset,
            "message": e.msg,
            "code_snippet": e.text.strip() if e.text else ""
        }
    except IndentationError as e:
        return {
            "file": str(file_path.relative_to(get_workspace_root())),
            "line": e.lineno,
            "column": e.offset,
            "message": f"IndentationError: {e.msg}",
            "code_snippet": e.text.strip() if e.text else ""
        }
    except UnicodeDecodeError:
        return {
            "file": str(file_path.relative_to(get_workspace_root())),
            "line": 0,
            "column": 0,
            "message": "UnicodeDecodeError: File must be UTF-8 encoded",
            "code_snippet": ""
        }
    except Exception as e:
        return {
            "file": str(file_path.relative_to(get_workspace_root())),
            "line": 0,
            "column": 0,
            "message": f"Unexpected error: {str(e)}",
            "code_snippet": ""
        }

def run_check():
    """
    Main execution logic.
    """
    start_time = time.time()
    root = get_workspace_root()
    files_checked = 0
    violations = []
    
    # scan directories
    for dir_name in TARGET_DIRECTORIES:
        target_dir = root / dir_name
        if not target_dir.exists():
            continue
            
        for path in target_dir.rglob("*.py"):
            # Check ignored directories
            if any(part in IGNORE_DIRS for part in path.parts):
                continue
                
            files_checked += 1
            error = scan_file(path)
            if error:
                violations.append(error)

    # scan specific root files
    for file_name in TARGET_FILES:
        target_file = root / file_name
        if target_file.exists():
            files_checked += 1
            error = scan_file(target_file)
            if error:
                violations.append(error)
    
    # Prepare result
    status = "ready" if not violations else "error"
    message = "Syntax valid" if status == "ready" else f"{len(violations)} syntax errors detected"
    
    report = {
        "category": TOOL_CATEGORY,
        "status": status,
        "timestamp": _get_timestamp(),
        "metrics": {
            "duration_ms": round((time.time() - start_time) * 1000, 2)
        },
        "results": {
            "files_checked": files_checked,
            "syntax_errors": len(violations),
            "scanned_directories": TARGET_DIRECTORIES,
            "violations": violations
        },
        "message": message,
        "actionable": status == "error",
        "remediation": "Fix syntax errors at reported lines." if status == "error" else None
    }
    
    return report

# ------------------------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        report = run_check()
        print(json.dumps(report, indent=2, sort_keys=True))
        sys.exit(0 if report["status"] == "ready" else 1)
    except Exception as e:
        # Fallback for catastrophic failure
        fallback = {
            "category": TOOL_CATEGORY,
            "status": "error",
            "timestamp": _get_timestamp(),
            "results": {
                "files_checked": 0,
                "syntax_errors": 0,
                "violations": []
            },
            "message": f"Tool crashed: {str(e)}",
            "actionable": True,
            "remediation": "Debug python_syntax_check.py"
        }
        print(json.dumps(fallback, indent=2, sort_keys=True))
        sys.exit(1)
