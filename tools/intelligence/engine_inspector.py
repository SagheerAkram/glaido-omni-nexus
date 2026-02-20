"""
Engine Inspector
Reads offline engine snapshot and prints structured internal diagnostics.
"""

import sys
import json
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

        lines = []
        lines.append("==================================================")
        lines.append("      OMNI-NEXUS ENGINE INSPECTOR DIAGNOSTICS      ")
        lines.append("==================================================")
        lines.append(f"Timestamp: {data.get('timestamp')}")
        lines.append("")
        
        metrics = data.get("metrics", {})
        lines.append(f"[ INTEGRITY METRICS ]")
        lines.append(f"  Score:           {metrics.get('integrity_score')}%")
        lines.append(f"  Stability Index: {metrics.get('stability_index')}%")
        lines.append(f"  Structural Risk: {metrics.get('structural_risk_level')}")
        lines.append(f"  Tools Passed:    {metrics.get('tools_passed')}/{metrics.get('total_tools_verified')}")
        lines.append(f"  Compute Time:    {metrics.get('duration_ms')}ms")
        lines.append("")
        
        struct = data.get("structure", {})
        lines.append(f"[ STRUCTURE GRAPH ]")
        lines.append(f"  Total Files:     {struct.get('total_files')}")
        lines.append(f"  Total Dirs:      {struct.get('total_directories')}")
        
        lines.append("  Layers:")
        for layer, count in struct.get("layers", {}).items():
            if count > 0:
                lines.append(f"    - {layer}: {count} files")
                
        lines.append("  Boundaries:")
        for boundary in struct.get("boundaries", []):
            lines.append(f"    - {boundary}")
            
        lines.append("==================================================")
        
        inspector_output = "\n".join(lines)
        status = "ready"
        message = "Engine inspected successfully."
        results = {
            "inspector_output": inspector_output,
            "metrics": metrics,
            "structure": struct
        }
    except Exception as e:
        status = "error"
        message = "Failed to inspect engine."
        results = {"error": str(e)}
        
    return {
        "category": "engine_inspector",
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
