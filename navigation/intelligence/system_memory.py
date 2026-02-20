"""
System Memory
Offline-first file-based JSON state storage for the intelligence engine.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from navigation.intelligence.contracts import EngineSnapshot

def get_memory_file_path() -> Path:
    """Get the path to the system memory JSON file."""
    memory_dir = Path(__file__).resolve().parents[2] / ".glaido"
    memory_dir.mkdir(parents=True, exist_ok=True)
    return memory_dir / "system_memory.json"

def write_snapshot(snapshot: EngineSnapshot) -> None:
    """Store the latest verification snapshot to offline memory."""
    memory_path = get_memory_file_path()
    with open(memory_path, 'w', encoding='utf-8') as f:
        json.dump(snapshot.to_dict(), f, indent=2, sort_keys=True)

import time
from datetime import datetime, timezone

def read_latest_snapshot() -> Optional[Dict[str, Any]]:
    """Read the latest verification snapshot from offline memory."""
    memory_path = get_memory_file_path()
    if not memory_path.exists():
        return None
        
    try:
        with open(memory_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

def run_check() -> Dict[str, Any]:
    """Validate system memory offline access."""
    start_time = time.time()
    try:
        memory_path = get_memory_file_path()
        status = "ready"
        message = "System memory accessible."
        results = {
            "memory_path": str(memory_path),
            "exists": memory_path.exists()
        }
        if memory_path.exists():
            results["size_bytes"] = memory_path.stat().st_size
    except Exception as e:
        status = "error"
        message = "System memory check failed."
        results = {"error": str(e)}
        
    return {
        "category": "system_memory",
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": message,
        "actionable": status == "error",
        "remediation": "Check directory permissions for .glaido/" if status == "error" else None,
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
