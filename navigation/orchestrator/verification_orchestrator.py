"""
Verification Orchestrator

Minimal orchestrator that sequentially runs all verification tools.
Derived from: architecture/sops/link_verification_protocol.md

This orchestrator contains NO decision logic, routing trees, or priority systems.
It simply runs tools in sequence and aggregates results.
"""

import sys
import json
import subprocess
from pathlib import Path


def get_workspace_root():
    """Get workspace root directory"""
    return Path(__file__).resolve().parents[2]


def run_verification_tool(tool_path):
    """
    Execute a verification tool and return its JSON output.
    
    Args:
        tool_path: Path to the verification tool
        
    Returns:
        dict: Parsed JSON output from tool
    """
    try:
        result = subprocess.run(
            [sys.executable, str(tool_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Parse JSON output
        output = json.loads(result.stdout)
        
        # Add execution metadata
        output["exit_code"] = result.returncode
        output["executed"] = True
        
        return output
        
    except subprocess.TimeoutExpired:
        return {
            "category": "unknown",
            "status": "error",
            "executed": False,
            "error": "Tool execution timeout"
        }
    except json.JSONDecodeError as e:
        return {
            "category": "unknown",
            "status": "error",
            "executed": False,
            "error": f"Invalid JSON output: {str(e)}"
        }
    except Exception as e:
        return {
            "category": "unknown",
            "status": "error",
            "executed": False,
            "error": str(e)
        }


def run_sequential_verification():
    """
    Run all verification tools in sequential order.
    No decision logic - just linear execution.
    """
    workspace = get_workspace_root()

    # Finalized Pipeline Execution Order
    tools = [
        ("local_dependencies",    workspace / "tools/core/local_dependency_check.py"),
        ("workspace_hygiene",     workspace / "tools/core/workspace_hygiene_check.py"),
        ("python_syntax",         workspace / "tools/core/python_syntax_check.py"),
        ("ant_boundary",          workspace / "tools/core/ant_boundary_enforcer.py"),
        ("orphaned_tools",        workspace / "tools/core/orphaned_tool_verifier.py"),
        ("architecture_links",    workspace / "tools/core/architecture_link_validator.py"),
        ("filesystem_integrity",  workspace / "tools/core/filesystem_integrity_check.py"),
        ("python_packages",       workspace / "tools/core/python_package_check.py"),
        ("schema_validation",     workspace / "tools/core/schema_validator_stub.py"),
        ("agent_registry",        workspace / "tools/agents/registry_readiness_check.py"),
    ]
    
    # Execute each tool sequentially
    results = {}
    for category, tool_path in tools:
        results[category] = run_verification_tool(tool_path)
    
    # Aggregate overall status (no complex logic, just basic check)
    all_executed = all(r.get("executed", False) for r in results.values())
    all_passed = all(
        r.get("status") in ["ready", "healthy"] 
        for r in results.values()
    )
    
    overall_status = "ready" if all_executed and all_passed else "not_ready"
    
    # Build aggregated report
    report = {
        "orchestrator": "verification_orchestrator",
        "overall_status": overall_status,
        "verifications": results,
        "execution_order": [category for category, _ in tools]
    }
    
    return report


if __name__ == "__main__":
    result = run_sequential_verification()
    print(json.dumps(result, indent=2, sort_keys=True))
    
    # Exit with status
    sys.exit(0 if result["overall_status"] == "ready" else 1)
