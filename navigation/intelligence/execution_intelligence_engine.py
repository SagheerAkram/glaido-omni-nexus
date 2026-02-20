"""
Execution Intelligence Engine
Consumes orchestrator results and calculates health scores.
Transforms verification output into an EngineSnapshot.
"""

from datetime import datetime, timezone
import json
from typing import Dict, Any

from navigation.intelligence.contracts import (
    EngineSnapshot, IntegrityMetrics, PipelineState, StructureGraph
)
from navigation.intelligence.repo_structure_analyzer import analyze_structure

def calculate_integrity(pipeline_data: Dict[str, Any]) -> IntegrityMetrics:
    """Calculate health scores from orchestrator output."""
    verifications = pipeline_data.get("verifications", {})
    
    total_tools = len(verifications)
    tools_passed = 0
    total_duration = 0.0
    
    for _, result in verifications.items():
        if result.get("status") in ["ready", "healthy"]:
            tools_passed += 1
        total_duration += result.get("metrics", {}).get("duration_ms", 0)
        
    # Calculate Scores
    integrity_score = (tools_passed / total_tools if total_tools > 0 else 0.0) * 100
    
    # Stability: based on timeout failures/execution errors vs total success
    # For now, it mirrors integrity but could weigh duration or fallback states
    stability_index = integrity_score
    
    if integrity_score == 100.0:
        structural_risk_level = "NONE"
    elif integrity_score >= 80.0:
        structural_risk_level = "LOW"
    elif integrity_score >= 50.0:
        structural_risk_level = "MODERATE"
    else:
        structural_risk_level = "CRITICAL"
        
    return IntegrityMetrics(
        integrity_score=round(integrity_score, 2),
        stability_index=round(stability_index, 2),
        structural_risk_level=structural_risk_level,
        total_tools_verified=total_tools,
        tools_passed=tools_passed,
        duration_ms=round(total_duration, 2)
    )

import time

def consume_orchestrator_output(raw_output: str) -> EngineSnapshot:
    """Parse output from verification orchestrator and build a full snapshot."""
    try:
        pipeline_data = json.loads(raw_output)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse orchestrator output: {e}")
        
    pipeline_state = PipelineState(
        orchestrator=pipeline_data.get("orchestrator", "unknown"),
        overall_status=pipeline_data.get("overall_status", "not_ready"),
        execution_order=pipeline_data.get("execution_order", []),
        verifications=pipeline_data.get("verifications", {})
    )
    
    metrics = calculate_integrity(pipeline_data)
    structure = analyze_structure()
    
    return EngineSnapshot(
        timestamp=datetime.now(timezone.utc).isoformat(),
        pipeline_state=pipeline_state,
        metrics=metrics,
        structure=structure
    )

def run_check() -> Dict[str, Any]:
    """Execute engine health check independent of the orchestrator."""
    start_time = time.time()
    try:
        from navigation.intelligence.system_memory import read_latest_snapshot
        snapshot_data = read_latest_snapshot()
        if snapshot_data:
            status = "ready"
            message = "Execution engine operational. Latest snapshot loaded."
            results = {
                "latest_snapshot_timestamp": snapshot_data.get("timestamp"),
                "metrics": snapshot_data.get("metrics")
            }
        else:
            status = "healthy"
            message = "Execution engine operational. No snapshot found."
            results = {"latest_snapshot_timestamp": None}
    except Exception as e:
        status = "error"
        message = "Execution engine check failed."
        results = {"error": str(e)}
        
    return {
        "category": "execution_intelligence_engine",
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": message,
        "actionable": status == "error",
        "remediation": "Verify intelligence modules integration." if status == "error" else None,
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
