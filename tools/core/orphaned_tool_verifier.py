#!/usr/bin/env python3
import sys
import json
import time
import ast
from datetime import datetime, timezone
from pathlib import Path

def get_workspace_root() -> Path:
    return Path(__file__).resolve().parents[2]

def get_registered_tools(orchestrator_path: Path) -> set:
    registered = set()
    try:
        with open(orchestrator_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if node.value.endswith(".py"):
                    registered.add(node.value.split("/")[-1])
            # Fallback for Python versions prior to 3.8
            elif isinstance(node, getattr(ast, 'Str', type(None))):
                if node.s.endswith(".py"):
                    registered.add(node.s.split("/")[-1])
    except Exception:
        pass
    return registered

def run_check():
    start_time = time.perf_counter_ns()
    workspace = get_workspace_root()
    
    orchestrator_path = workspace / "navigation" / "orchestrator" / "verification_orchestrator.py"
    tools_dir = workspace / "tools" / "core"
    
    violations = []
    
    if orchestrator_path.exists() and tools_dir.exists():
        actual_tools = {p.name for p in tools_dir.glob("*.py") if p.name != "__init__.py"}
        registered_tools = get_registered_tools(orchestrator_path)
        
        # Tools permitted to exist without explicit verification orchestration:
        # e.g., validator.py (used as a stub import)
        whitelist = {"validator.py", "diagnostics.py", "json_contract_validator.py", "base_tool_contract.py"}
        
        orphans = actual_tools - registered_tools - whitelist
        
        for orphan in orphans:
            violations.append({
                "file": orphan,
                "reason": "Present in tools/core/ but not registered in verification_orchestrator.py list"
            })
            
    duration_ms = (time.perf_counter_ns() - start_time) // 1_000_000
    status = "ready" if not violations else "error"
    message = "All tools registered" if not violations else f"{len(violations)} orphaned tools detected"
    
    report = {
        "category": "orphaned_tools",
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": message,
        "actionable": bool(violations),
        "remediation": "Add orphaned tools to verification_orchestrator.py or remove them to maintain integrity" if violations else None,
        "results": {
            "violations": violations
        },
        "metrics": {
            "duration_ms": duration_ms
        }
    }
    
    return report

if __name__ == "__main__":
    try:
        report = run_check()
        print(json.dumps(report, sort_keys=True))
        sys.exit(0 if report["status"] == "ready" else 1)
    except Exception as e:
        fallback = {
            "category": "pipeline_integrity",
            "status": "error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": "Critical failure in pipeline integrity verifier",
            "actionable": True,
            "remediation": "Check orphaned_tool_verifier.py logic",
            "results": {"error": str(e)}
        }
        print(json.dumps(fallback, sort_keys=True))
        sys.exit(1)
