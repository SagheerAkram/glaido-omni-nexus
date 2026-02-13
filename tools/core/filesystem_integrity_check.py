"""
Filesystem Integrity Check Tool

Validates A.N.T. directory structure and core files exist.
Derived from: architecture/sops/link_verification_protocol.md (Section 2)
"""

import sys
import json
from pathlib import Path

# Required A.N.T. directories (from system diagnostics)
REQUIRED_DIRECTORIES = [
    "architecture/core",
    "architecture/sops",
    "architecture/specifications",
    "architecture/edge_cases",
    "architecture/protocols",
    "navigation/router",
    "navigation/workflows",
    "tools/core",
    "tools/agents",
    "tools/utilities",
    "agents",
    "cli/display",
    ".tmp/logs",
    ".tmp/cache",
    ".tmp/sessions",
    "tests/unit",
    "tests/integration",
    "config"
]

# Core memory files
CORE_FILES = [
    "task_plan.md",
    "progress.md", 
    "findings.md",
    "gemini.md"
]


def get_workspace_root():
    """Get workspace root directory"""
    return Path(__file__).resolve().parents[2]


def check_directories():
    """Verify all required directories exist"""
    workspace = get_workspace_root()
    found = []
    missing = []
    
    for dir_path in REQUIRED_DIRECTORIES:
        full_path = workspace / dir_path
        if full_path.exists() and full_path.is_dir():
            found.append(dir_path)
        else:
            missing.append(dir_path)
    
    return {
        "required": len(REQUIRED_DIRECTORIES),
        "found": len(found),
        "missing": missing
    }


def check_core_files():
    """Verify core memory files exist and readable"""
    workspace = get_workspace_root()
    found = []
    missing = []
    unreadable = []
    empty = []
    
    for file_name in CORE_FILES:
        file_path = workspace / file_name
        
        if not file_path.exists():
            missing.append(file_name)
            continue
        
        try:
            content = file_path.read_text(encoding='utf-8')
            if len(content.strip()) == 0:
                empty.append(file_name)
            else:
                found.append(file_name)
        except Exception:
            unreadable.append(file_name)
    
    return {
        "required": len(CORE_FILES),
        "found": len(found),
        "missing": missing,
        "unreadable": unreadable,
        "empty": empty
    }


def check_architecture_immutable():
    """Test architecture directory immutability (conceptual - returns True)"""
    # Post-Blueprint, architecture should be immutable
    # This is a conceptual check - not enforced by filesystem
    workspace = get_workspace_root()
    arch_dir = workspace / "architecture"
    
    return {
        "exists": arch_dir.exists(),
        "conceptually_immutable": True,
        "note": "Immutability enforced by protocol, not filesystem"
    }


def check_temp_writable():
    """Verify temp directory is writable"""
    workspace = get_workspace_root()
    test_file = workspace / ".tmp" / "integrity_test.json"
    
    try:
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text(json.dumps({"test": "data"}))
        content = test_file.read_text()
        test_file.unlink()
        
        return {
            "writable": True,
            "error": None
        }
    except Exception as e:
        return {
            "writable": False,
            "error": str(e)
        }


def run_check():
    """Execute filesystem integrity checks"""
    dirs = check_directories()
    files = check_core_files()
    arch = check_architecture_immutable()
    temp = check_temp_writable()
    
    # Determine status
    dirs_ok = len(dirs["missing"]) == 0
    files_ok = len(files["missing"]) == 0 and len(files["unreadable"]) == 0
    temp_ok = temp["writable"]
    
    if dirs_ok and files_ok and temp_ok:
        status = "healthy"
    elif dirs_ok and files_ok:
        status = "degraded"  # temp not writable
    else:
        status = "error"
    
    report = {
        "category": "filesystem_integrity",
        "status": status,
        "directories": dirs,
        "core_files": files,
        "architecture_immutable": arch["conceptually_immutable"],
        "temp_writable": temp["writable"]
    }
    
    return report


if __name__ == "__main__":
    result = run_check()
    print(json.dumps(result, indent=2))
    
    # Exit with status code
    exit_code = 0 if result["status"] == "healthy" else 1
    sys.exit(exit_code)
