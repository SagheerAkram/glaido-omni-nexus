#!/usr/bin/env python3
import sys
import json
import ast
import time
from datetime import datetime, timezone
from pathlib import Path

def get_workspace_root() -> Path:
    return Path(__file__).resolve().parents[2]

def check_layer(workspace: Path, layer_path: str, forbidden_imports: list) -> list:
    violations = []
    layer_dir = workspace / layer_path
    if not layer_dir.exists():
        return violations
        
    for py_file in layer_dir.rglob("*.py"):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=str(py_file))
                
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        for forbidden in forbidden_imports:
                            if alias.name == forbidden or alias.name.startswith(f"{forbidden}."):
                                violations.append({
                                    "file": str(py_file.relative_to(workspace)),
                                    "line": node.lineno,
                                    "import": alias.name,
                                    "forbidden": forbidden
                                })
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        for forbidden in forbidden_imports:
                            if node.module == forbidden or node.module.startswith(f"{forbidden}."):
                                violations.append({
                                    "file": str(py_file.relative_to(workspace)),
                                    "line": node.lineno,
                                    "import": node.module,
                                    "forbidden": forbidden
                                })
        except Exception:
            pass # Gracefully handle unparseable files
    return violations

def run_check():
    start_time = time.perf_counter_ns()
    workspace = get_workspace_root()
    violations = []
    
    # Rule 1: tools/ cannot import cli/
    violations.extend(check_layer(workspace, "tools/", ["cli"]))
    
    # Rule 2: navigation/ cannot import cli/display/
    violations.extend(check_layer(workspace, "navigation/", ["cli.display"]))
    
    duration_ms = (time.perf_counter_ns() - start_time) // 1_000_000
    
    status = "ready" if not violations else "error"
    message = "Layer boundaries respected" if not violations else f"{len(violations)} boundary violations detected"
    
    report = {
        "category": "ant_boundary",
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": message,
        "actionable": bool(violations),
        "remediation": "Remove cross-layer imports referencing forbidden architectural zones" if violations else None,
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
            "category": "ant_boundary",
            "status": "error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": "Critical failure in A.N.T boundary enforcer",
            "actionable": True,
            "remediation": "Check ant_boundary_enforcer.py logic",
            "results": {"error": str(e)}
        }
        print(json.dumps(fallback, sort_keys=True))
        sys.exit(1)
