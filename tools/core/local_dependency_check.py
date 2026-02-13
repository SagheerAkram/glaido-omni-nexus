"""
Local Dependency Check Tool

Verifies Python runtime and standard library availability.
Derived from: architecture/sops/link_verification_protocol.md (Section 1)
"""

import sys
import json
from pathlib import Path

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
    python_check = check_python_version()
    modules_check = check_required_modules()
    filesystem_check = check_filesystem_writable()
    
    # Determine overall status
    all_ready = (
        python_check["meets_requirement"] and
        modules_check["all_available"] and
        filesystem_check["writable"]
    )
    
    report = {
        "category": "local_dependencies",
        "status": "ready" if all_ready else "not_ready",
        "python_version": python_check,
        "modules": modules_check,
        "filesystem": filesystem_check
    }
    
    return report


if __name__ == "__main__":
    result = run_check()
    print(json.dumps(result, indent=2))
    
    # Exit with non-zero if not ready
    sys.exit(0 if result["status"] == "ready" else 1)
