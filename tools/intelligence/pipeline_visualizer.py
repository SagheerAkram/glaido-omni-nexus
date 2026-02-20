"""
Pipeline Visualizer
Generates an ASCII pipeline map dynamically based on orchestrator order.
"""

import sys
import io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from pathlib import Path
import time
from datetime import datetime, timezone

def get_workspace_root() -> Path:
    return Path(__file__).resolve().parents[2]

sys.path.insert(0, str(get_workspace_root()))
from navigation.intelligence.system_memory import read_latest_snapshot

def run_check() -> dict:
    start_time = time.time()
    try:
        data = read_latest_snapshot()
        if not data:
            raise ValueError("No engine snapshot found. Run verification pipeline first.")
            
        pipeline = data.get("pipeline_state", {})
        order = pipeline.get("execution_order", [])
        verifications = pipeline.get("verifications", {})
        
        lines = []
        lines.append("==================================================")
        lines.append("           PIPELINE EXECUTION TOPOLOGY            ")
        lines.append("==================================================")
        
        if not order:
            lines.append("Pipeline is empty.")
        else:
            for i, step in enumerate(order):
                info = verifications.get(step, {})
                step_status = info.get("status", "unknown")
                
                icon = "[✓]" if step_status in ["ready", "healthy"] else "[X]"
                
                lines.append(f"    {icon} {step}")
                if i < len(order) - 1:
                    lines.append("     |")
                    lines.append("     v")
                    
        lines.append("==================================================")
        lines.append(f"Pipeline Overall Status: {pipeline.get('overall_status', 'unknown').upper()}")
        
        ascii_map = "\n".join(lines)
        
        status = "ready"
        message = "Pipeline visualized successfully."
        results = {
            "ascii_map": ascii_map,
            "order": order
        }
    except Exception as e:
        status = "error"
        message = "Failed to visualize pipeline."
        results = {"error": str(e)}
        
    return {
        "category": "pipeline_visualizer",
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": message,
        "actionable": status == "error",
        "remediation": "Run the verification pipeline to generate snapshot." if status == "error" else None,
        "results": results,
        "metrics": {
            "duration_ms": round((time.time() - start_time) * 1000, 2)
        }
    }

if __name__ == "__main__":
    report = run_check()
    print(json.dumps(report, indent=2, sort_keys=True))
    sys.exit(0 if report["status"] in ["ready", "healthy"] else 1)
