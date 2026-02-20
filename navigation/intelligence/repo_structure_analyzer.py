"""
Repository Structure Analyzer
Scans the project tree to build a structural graph of layers, modules, and boundaries.
Returns deterministic JSON insights via StructureGraph contract.
"""

from pathlib import Path
import time
from datetime import datetime, timezone
import json
from typing import Dict, List, Set, Any
from navigation.intelligence.contracts import StructureGraph

def get_workspace_root() -> Path:
    return Path(__file__).resolve().parents[2]

def analyze_structure() -> StructureGraph:
    """Scan the repository and build a deterministic structural graph."""
    workspace = get_workspace_root()
    
    total_files = 0
    total_directories = 0
    
    layer_counts: Dict[str, int] = {
        "tools": 0,
        "navigation": 0,
        "architecture": 0,
        "cli": 0
    }
    
    modules: Set[str] = set()
    boundaries: List[str] = [
        "Intelligence Wall (tools/core no AI)",
        "Linear Pipeline (orchestrator execution)",
        "Output Determinism (CLI JSON rendering)"
    ]
    
    # Exclude common ignores
    excludes = {".git", "__pycache__", "venv", ".glaido"}
    
    for path in workspace.rglob("*"):
        if any(part in excludes for part in path.parts):
            continue
            
        if path.is_file():
            total_files += 1
            if path.suffix == ".py":
                # Check layer
                rel_parts = path.relative_to(workspace).parts
                if len(rel_parts) > 1:
                    layer = rel_parts[0]
                    if layer in layer_counts:
                        layer_counts[layer] += 1
                    
                    if len(rel_parts) > 2:
                        # Consider subdirectories as modules (e.g. tools/core, navigation/intelligence)
                        modules.add(f"{rel_parts[0]}/{rel_parts[1]}")
                        
        elif path.is_dir():
            total_directories += 1

    return StructureGraph(
        total_files=total_files,
        total_directories=total_directories,
        layers=layer_counts,
        modules=sorted(list(modules)),
        boundaries=boundaries
    )

def run_check() -> Dict[str, Any]:
    """Execute structural analysis and return standardized report."""
    start_time = time.time()
    try:
        graph = analyze_structure()
        results = {
            "total_files": graph.total_files,
            "total_directories": graph.total_directories,
            "layers": graph.layers,
            "modules": graph.modules,
            "boundaries": graph.boundaries
        }
        status = "ready"
        message = "Repository structure analyzed successfully."
        error_msg = None
    except Exception as e:
        status = "error"
        message = "Failed to analyze repository structure."
        results = {"error": str(e)}
        error_msg = str(e)
        
    return {
        "category": "repo_structure_analyzer",
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": message,
        "actionable": status == "error",
        "remediation": "Check for filesystem permission issues." if status == "error" else None,
        "results": results,
        "metrics": {
            "duration_ms": round((time.time() - start_time) * 1000, 2)
        }
    }

if __name__ == "__main__":
    import sys
    report = run_check()
    print(json.dumps(report, indent=2, sort_keys=True))
    sys.exit(0 if report["status"] in ["ready", "healthy"] else 1)
