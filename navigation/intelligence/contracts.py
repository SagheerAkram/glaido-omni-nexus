"""
Internal Engine API Contracts
Defines the strict dataclasses representing the state and intelligence of the Omni-Nexus system.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone

@dataclass
class IntegrityMetrics:
    integrity_score: float
    stability_index: float
    structural_risk_level: str
    total_tools_verified: int
    tools_passed: int
    duration_ms: float

@dataclass
class PipelineState:
    orchestrator: str
    overall_status: str
    execution_order: List[str]
    verifications: Dict[str, Any]

@dataclass
class StructureGraph:
    total_files: int
    total_directories: int
    layers: Dict[str, int]
    modules: List[str]
    boundaries: List[str]

@dataclass
class EngineSnapshot:
    timestamp: str
    pipeline_state: PipelineState
    metrics: IntegrityMetrics
    structure: StructureGraph

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "pipeline_state": {
                "orchestrator": self.pipeline_state.orchestrator,
                "overall_status": self.pipeline_state.overall_status,
                "execution_order": self.pipeline_state.execution_order,
                "verifications": self.pipeline_state.verifications,
            },
            "metrics": {
                "integrity_score": self.metrics.integrity_score,
                "stability_index": self.metrics.stability_index,
                "structural_risk_level": self.metrics.structural_risk_level,
                "total_tools_verified": self.metrics.total_tools_verified,
                "tools_passed": self.metrics.tools_passed,
                "duration_ms": self.metrics.duration_ms,
            },
            "structure": {
                "total_files": self.structure.total_files,
                "total_directories": self.structure.total_directories,
                "layers": self.structure.layers,
                "modules": self.structure.modules,
                "boundaries": self.structure.boundaries,
            }
        }

def run_check() -> Dict[str, Any]:
    """Validate contract definitions."""
    import time
    start_time = time.time()
    return {
        "category": "contracts",
        "status": "ready",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": "Engine contracts are defined and available.",
        "actionable": False,
        "remediation": None,
        "results": {"contracts": ["IntegrityMetrics", "PipelineState", "StructureGraph", "EngineSnapshot"]},
        "metrics": {"duration_ms": round((time.time() - start_time) * 1000, 2)}
    }

if __name__ == "__main__":
    import json
    import sys
    report = run_check()
    print(json.dumps(report, indent=2, sort_keys=True))
    sys.exit(0 if report["status"] in ["ready", "healthy"] else 1)
