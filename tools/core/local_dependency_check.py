"""
Local Dependency Check Tool

Verifies Python runtime and standard library availability.
Derived from: architecture/sops/link_verification_protocol.md (Section 1)
"""

import sys
import json
import time
from datetime import datetime, timezone
from pathlib import Path

def _get_timestamp():
    """Return ISO 8601 timestamp with timezone"""
    return datetime.now(timezone.utc).astimezone().isoformat()

# Required standard library modules for Omni-Nexus
REQUIRED_MODULES = [
    'json',
    'pathlib',
    'sys',
    'shutil',
    'datetime',
    'argparse',
    'subprocess'
]

# Minimum Python version
MIN_PYTHON_VERSION = (3, 8)


def check_python_version():
    """Check Python version meets minimum requirement"""
    current = sys.version_info[:2]
    meets_requirement = current >= MIN_PYTHON_VERSION
    
    return {
        "current": f"{current[0]}.{current[1]}",
        "required": f"{MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}",
        "meets_requirement": meets_requirement
    }


def check_required_modules():
    """Verify all required standard library modules are importable"""
    missing = []
    available = []
    
    for module_name in REQUIRED_MODULES:
        try:
            __import__(module_name)
            available.append(module_name)
        except ImportError:
            missing.append(module_name)
    
    return {
        "required": REQUIRED_MODULES,
        "available": available,
        "missing": missing,
        "all_available": len(missing) == 0
    }


def check_filesystem_writable():
    """Test write permissions to workspace"""
    workspace_root = Path(__file__).resolve().parents[2]
    test_file = workspace_root / '.tmp' / 'dependency_test.txt'
    
    try:
        # Ensure .tmp exists
        test_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write test
        test_file.write_text("dependency_check_test")
        
        # Read test
        content = test_file.read_text()
        
        # Cleanup
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
    """Execute all local dependency checks"""
    start_time = time.time()
    python_check = check_python_version()
    modules_check = check_required_modules()
    filesystem_check = check_filesystem_writable()
    
    # Determine overall status
    all_ready = (
        python_check["meets_requirement"] and
        modules_check["all_available"] and
        filesystem_check["writable"]
    )
    status = "ready" if all_ready else "error"
    
    report = {
        "category": "local_dependencies",
        "status": status,
        "timestamp": _get_timestamp(),
        "metrics": {
            "duration_ms": round((time.time() - start_time) * 1000, 2)
        },
        "results": {
            "python_version": python_check,
            "modules": modules_check,
            "filesystem": filesystem_check
        },
        "message": "Local dependencies verified" if status == "ready" else "Local dependency failure",
        "actionable": status == "error",
        "remediation": "Check python version and pip modules" if status == "error" else None
    }
    
    return report


if __name__ == "__main__":
    result = run_check()
    print(json.dumps(result, indent=2, sort_keys=True))
    
    # Exit with non-zero if not ready
    sys.exit(0 if result["status"] == "ready" else 1)
