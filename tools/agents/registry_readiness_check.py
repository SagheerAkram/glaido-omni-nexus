"""
Registry Readiness Check Tool

Verifies agent registry initialized and operational.
Derived from: architecture/sops/link_verification_protocol.md (Section 4)
"""

import sys
import json
from pathlib import Path


def get_registry_path():
    """Get path to agent registry"""
    workspace = Path(__file__).resolve().parents[2]
    return workspace / "agents" / "_registry.json"


def check_registry_exists():
    """Verify registry file exists"""
    registry_path = get_registry_path()
    
    return {
        "path": str(registry_path),
        "exists": registry_path.exists()
    }


def check_registry_valid_json():
    """Validate registry is parseable JSON"""
    registry_path = get_registry_path()
    
    if not registry_path.exists():
        return {
            "valid": False,
            "error": "File does not exist"
        }
    
    try:
        content = registry_path.read_text(encoding='utf-8')
        data = json.loads(content)
        
        return {
            "valid": True,
            "data": data,
            "error": None
        }
    except json.JSONDecodeError as e:
        return {
            "valid": False,
            "error": f"JSON parsing failed: {str(e)}"
        }
    except Exception as e:
        return {
            "valid": False,
            "error": str(e)
        }


def check_registry_structure(data):
    """Verify registry has required structure"""
    if data is None:
        return {
            "valid_structure": False,
            "error": "No data provided"
        }
    
    # Check for required top-level fields
    has_agents = "agents" in data
    agents_is_list = isinstance(data.get("agents", []), list)
    
    # Check each agent entry
    valid_agents = True
    agent_count = 0
    
    if has_agents and agents_is_list:
        agent_count = len(data["agents"])
        for agent in data["agents"]:
            required_fields = ["agent_id", "name", "type", "path", "status"]
            if not all(field in agent for field in required_fields):
                valid_agents = False
                break
    
    return {
        "valid_structure": has_agents and agents_is_list and valid_agents,
        "has_agents_field": has_agents,
        "agents_is_list": agents_is_list,
        "agent_count": agent_count,
        "all_agents_valid": valid_agents
    }


def check_registry_writable():
    """Test registry write access (without modifying)"""
    registry_path = get_registry_path()
    temp_test = registry_path.parent / "_registry_test.json"
    
    try:
        # Test write to temporary file in same directory
        test_data = {"test": "data"}
        temp_test.write_text(json.dumps(test_data, indent=2))
        
        # Verify written correctly
        verify = json.loads(temp_test.read_text())
        
        # Cleanup
        temp_test.unlink()
        
        return {
            "writable": True,
            "error": None
        }
    except Exception as e:
        return {
            "writable": False,
            "error": str(e)
        }


def check_backup_functional():
    """Verify backup mechanism functional"""
    registry_path = get_registry_path()
    backup_path = registry_path.with_suffix('.json.bak')
    
    # Check if backup exists (indicates backup mechanism has run)
    backup_exists = backup_path.exists()
    
    # Check if backup is creatable
    test_backup = registry_path.parent / "_test_backup.json.bak"
    try:
        test_backup.write_text(json.dumps({"test": "backup"}))
        test_backup.unlink()
        backup_creatable = True
        error = None
    except Exception as e:
        backup_creatable = False
        error = str(e)
    
    return {
        "backup_exists": backup_exists,
        "backup_creatable": backup_creatable,
        "functional": backup_creatable,
        "error": error
    }


def run_check():
    """Execute agent registry readiness checks"""
    exists = check_registry_exists()
    valid_json = check_registry_valid_json()
    
    # Only check structure if JSON is valid
    if valid_json["valid"]:
        structure = check_registry_structure(valid_json["data"])
        agent_count = structure["agent_count"]
    else:
        structure = {"valid_structure": False}
        agent_count = 0
    
    writable = check_registry_writable()
    backup = check_backup_functional()
    
    # Determine status
    ready = (
        exists["exists"] and
        valid_json["valid"] and
        structure["valid_structure"] and
        writable["writable"] and
        backup["functional"]
    )
    
    report = {
        "category": "agent_registry",
        "status": "ready" if ready else "not_ready",
        "registry_exists": exists["exists"],
        "registry_valid_json": valid_json["valid"],
        "registry_valid_structure": structure["valid_structure"],
        "registry_writable": writable["writable"],
        "backup_functional": backup["functional"],
        "agent_count": agent_count,
        "errors": []
    }
    
    # Collect errors
    if not valid_json["valid"] and valid_json.get("error"):
        report["errors"].append(valid_json["error"])
    if not writable["writable"] and writable.get("error"):
        report["errors"].append(writable["error"])
    if not backup["functional"] and backup.get("error"):
        report["errors"].append(backup["error"])
    
    return report


if __name__ == "__main__":
    result = run_check()
    print(json.dumps(result, indent=2))
    
    # Exit with status
    sys.exit(0 if result["status"] == "ready" else 1)
