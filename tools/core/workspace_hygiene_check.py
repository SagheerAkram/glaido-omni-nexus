import os
import sys
import json
import time
import pathlib
import datetime

# --- Configuration & Spec ---
TOOL_CATEGORY = "workspace_hygiene"
VERSION = "1.0.0"

# Root Compliance
ALLOWED_ROOT_DIRS = {
    ".git", ".tmp", "agents", "architecture", "cli", 
    "config", "navigation", "tests", "tools",
    ".vscode", ".idea", "__pycache__" # IDE/System allowances
}

ALLOWED_ROOT_FILES = {
    ".gitignore", "LICENSE", "README.md", 
    "progress.md", "gemini.md", "task.md", 
    "findings.md", "task_plan.md", "requirements.txt"
}

ALLOWED_ROOT_EXTENSIONS = {".md"}

# Architecture Compliance
# architecture/ should primarily contain directories (layers)
ALLOWED_ARCH_FILES = {"README.md"} 

# Tools Compliance
# tools/ should primarily contain directories (categories)
# But .py files are allowed as direct utilities
ALLOWED_TOOLS_EXTENSIONS = {".py", ".md"}

def _get_timestamp():
    """Returns ISO 8601 timestamp with timezone awareness."""
    return datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()

def scan_root(root_path: pathlib.Path) -> list:
    violations = []
    
    # Iterate over all items in root
    for item in root_path.iterdir():
        name = item.name
        
        # 1. Directories
        if item.is_dir():
            if name not in ALLOWED_ROOT_DIRS:
                # Check if it's a known benign directory?
                # For now, strict enforcement based on spec.
                # Use a warning or strict violation? Spec says strict.
                violations.append({
                    "location": "root",
                    "path": name,
                    "rule": f"Unknown directory in root. Allowed: {sorted(list(ALLOWED_ROOT_DIRS))}"
                })
        
        # 2. Files
        elif item.is_file():
            if name in ALLOWED_ROOT_FILES:
                continue
            
            if item.suffix in ALLOWED_ROOT_EXTENSIONS:
                continue
                
            violations.append({
                "location": "root",
                "path": name,
                "rule": "Unknown file in root. Clean workspace required."
            })
            
    return violations

def scan_architecture(root_path: pathlib.Path) -> list:
    violations = []
    arch_path = root_path / "architecture"
    
    if not arch_path.exists():
        return [] # filesystem_integrity check handles missing dirs
        
    for item in arch_path.iterdir():
        if item.is_file():
            if item.name not in ALLOWED_ARCH_FILES:
                violations.append({
                    "location": "architecture",
                    "path": f"architecture/{item.name}",
                    "rule": "Architecture root should contain directories only (Layer separation)."
                })
    return violations

def scan_tools(root_path: pathlib.Path) -> list:
    violations = []
    tools_path = root_path / "tools"
    
    if not tools_path.exists():
        return []
        
    for item in tools_path.iterdir():
        if item.is_file():
            if item.suffix not in ALLOWED_TOOLS_EXTENSIONS:
                 violations.append({
                    "location": "tools",
                    "path": f"tools/{item.name}",
                    "rule": "Only .py script utilities allowed in tools root."
                })
    return violations

def run_check():
    """Main execution logic."""
    try:
        start_time = time.time()
        root_path = pathlib.Path.cwd()
        timestamp = _get_timestamp()
        
        all_violations = []
        
        # Execute Scans
        all_violations.extend(scan_root(root_path))
        all_violations.extend(scan_architecture(root_path))
        all_violations.extend(scan_tools(root_path))
        
        # Determine Status
        status = "ready" if not all_violations else "error"
        message = "Workspace hygiene verified." if status == "ready" else f"Workspace hygiene violations detected: {len(all_violations)} issues found."
        
        # Construct Report
        report = {
            "category": TOOL_CATEGORY,
            "status": status,
            "timestamp": timestamp,
            "metrics": {
                "duration_ms": round((time.time() - start_time) * 1000, 2)
            },
            "results": {
                "root_clean": len([v for v in all_violations if v['location'] == 'root']) == 0,
                "architecture_clean": len([v for v in all_violations if v['location'] == 'architecture']) == 0,
                "violations": all_violations
            },
            "message": message,
            "actionable": status == "error",
            "remediation": "Move files to appropriate subdirectories (.tmp/, config/, tools/) or delete them. See verification_operational_guidelines.md."
        }
        
        return report

    except Exception as e:
        # Fallback for catastrophic failure
        error_report = {
            "category": TOOL_CATEGORY,
            "status": "error",
            "timestamp": _get_timestamp(),
            "error": str(e),
            "message": "Internal tool error during hygiene check."
        }
        return error_report

if __name__ == "__main__":
    result = run_check()
    print(json.dumps(result, indent=2, sort_keys=True))
    
    # Exit with non-zero if not ready
    sys.exit(0 if result.get("status") == "ready" else 1)
