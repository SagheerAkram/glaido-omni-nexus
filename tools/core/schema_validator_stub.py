"""
Schema Validator Stub

Minimal schema validation readiness check.
Derived from: architecture/sops/link_verification_protocol.md (Section 3)

Note: This is a stub that verifies validator.py exists and is callable.
Actual schema validation logic already exists in tools/core/validator.py.
This tool checks that the validator is ready for use.
"""

import sys
import json
import time
from datetime import datetime, timezone
from pathlib import Path

def _get_timestamp():
    """Return ISO 8601 timestamp with timezone"""
    return datetime.now(timezone.utc).astimezone().isoformat()


def check_validator_exists():
    """Verify validator.py exists"""
    workspace = Path(__file__).resolve().parents[2]
    validator_path = workspace / "tools" / "core" / "validator.py"
    
    return {
        "path": str(validator_path),
        "exists": validator_path.exists()
    }


def check_validator_importable():
    """Test if validator can be imported"""
    try:
        # Add workspace root to sys.path to allow absolute imports
        workspace = Path(__file__).resolve().parents[2]
        if str(workspace) not in sys.path:
            sys.path.insert(0, str(workspace))

        # Attempt import
        import tools.core.validator as validator
        
        # Check validate function exists
        has_validate = hasattr(validator, 'validate')
        
        return {
            "importable": True,
            "has_validate_function": has_validate,
            "error": None
        }
    except Exception as e:
        return {
            "importable": False,
            "has_validate_function": False,
            "error": str(e)
        }


def check_schema_documentation():
    """Verify schema documentation exists"""
    workspace = Path(__file__).resolve().parents[2]
    schema_doc = workspace / "architecture" / "specifications" / "data_schemas.md"
    
    exists = schema_doc.exists()
    
    if exists:
        try:
            content = schema_doc.read_text(encoding='utf-8')
            # Check for expected schema types
            has_agent_config = "agent_config" in content
            has_tool_execution = "tool_execution" in content
            has_routing_decision = "routing_decision" in content
            
            return {
                "exists": True,
                "documented_schemas": {
                    "agent_config": has_agent_config,
                    "tool_execution": has_tool_execution,
                    "routing_decision": has_routing_decision
                }
            }
        except Exception as e:
            return {
                "exists": True,
                "error": str(e)
            }
    else:
        return {
            "exists": False
        }


def run_check():
    """Execute schema validation readiness checks"""
    start_time = time.time()
    validator_file = check_validator_exists()
    validator_import = check_validator_importable()
    schema_docs = check_schema_documentation()
    
    # Determine status
    ready = (
        validator_file["exists"] and
        validator_import["importable"] and
        validator_import["has_validate_function"] and
        schema_docs.get("exists", False)
    )
    status = "ready" if ready else "error"
    
    report = {
        "category": "schema_validation",
        "status": status,
        "timestamp": _get_timestamp(),
        "metrics": {
            "duration_ms": round((time.time() - start_time) * 1000, 2)
        },
        "results": {
            "validator_file": validator_file,
            "validator_import": validator_import,
            "schema_documentation": schema_docs
        },
        "message": "Schema validator stub verified" if status == "ready" else "Schema validator stub failed",
        "actionable": status == "error",
        "remediation": "Ensure tools/core/validator.py exists and handles valid schemas" if status == "error" else None
    }
    
    return report


if __name__ == "__main__":
    result = run_check()
    print(json.dumps(result, indent=2, sort_keys=True))
    
    # Exit with status
    sys.exit(0 if result["status"] == "ready" else 1)
