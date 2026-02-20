"""
Engine Status Provider
Provides a unified status view of the execution intelligence layer.
"""
import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional

def get_workspace_root() -> Path:
    return Path(__file__).resolve().parents[2]

sys.path.insert(0, str(get_workspace_root()))

from navigation.intelligence.system_memory import read_latest_snapshot, write_snapshot
from navigation.intelligence.execution_intelligence_engine import consume_orchestrator_output
from navigation.intelligence.contracts import EngineSnapshot

def build_engine_snapshot(orchestrator_json_output: str) -> EngineSnapshot:
    """Build a new engine snapshot from orchestrator output and save to memory."""
    snapshot = consume_orchestrator_output(orchestrator_json_output)
    write_snapshot(snapshot)
    return snapshot

def calculate_integrity_score() -> float:
    """Return the latest offline integrity score."""
    data = read_latest_snapshot()
    if not data:
        return 0.0
    return data.get("metrics", {}).get("integrity_score", 0.0)

def get_pipeline_overview() -> Dict[str, Any]:
    """Return an overview of the latest pipeline execution."""
    data = read_latest_snapshot()
    if not data:
        return {"status": "unknown", "message": "No snapshot found."}
    
    pipeline = data.get("pipeline_state", {})
    return {
        "overall_status": pipeline.get("overall_status", "unknown"),
        "total_tools": len(pipeline.get("execution_order", [])),
        "timestamp": data.get("timestamp", "unknown")
    }

def get_engine_status() -> dict:
    """Retrieve the current offline status of the intelligence engine."""
    score = calculate_integrity_score()
    overview = get_pipeline_overview()
    
    return {
        "status": "operational",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "intelligence_layer": "ACTIVE",
        "integrity_score": score,
        "latest_pipeline_status": overview.get("overall_status", "unknown"),
        "message": "Execution Intelligence Layer ascension complete."
    }

if __name__ == "__main__":
    print(json.dumps(get_engine_status(), indent=2, sort_keys=True))
