"""
Tool: System Diagnostics
Purpose: Health check and system introspection
Category: core
Created: 2026-02-13T21:04:24+05:00
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Add utilities to path
sys.path.append(str(Path(__file__).parent.parent / "utilities"))
from logger import info, warning, error

# Project root
PROJECT_ROOT = Path(__file__).parent.parent.parent


def check_directory_structure() -> Dict[str, Any]:
    """
    Verify A.N.T. directory structure is intact.
    
    Returns:
        Dict with status and missing directories
    """
    required_dirs = [
        "architecture",
        "architecture/core",
        "architecture/sops",
        "architecture/protocols",
        "architecture/specifications",
        "navigation",
        "navigation/orchestrator",
        "navigation/routing",
        "tools",
        "tools/core",
        "tools/utilities",
        "tools/agents",
        "agents",
        "cli",
        "cli/commands",
        "cli/display",
        ".tmp",
        ".tmp/logs",
        "config"
    ]
    
    missing = []
    for dir_path in required_dirs:
        full_path = PROJECT_ROOT / dir_path
        if not full_path.exists():
            missing.append(dir_path)
    
    return {
        "status": "healthy" if not missing else "degraded",
        "missing_directories": missing,
        "total_required": len(required_dirs),
        "total_found": len(required_dirs) - len(missing)
    }


def check_core_files() -> Dict[str, Any]:
    """
    Verify core project files exist.
    
    Returns:
        Dict with status and missing files
    """
    required_files = [
        "task_plan.md",
        "findings.md",
        "progress.md",
        "gemini.md"
    ]
    
    missing = []
    for file_path in required_files:
        full_path = PROJECT_ROOT / file_path
        if not full_path.exists():
            missing.append(file_path)
    
    return {
        "status": "healthy" if not missing else "degraded",
        "missing_files": missing,
        "total_required": len(required_files),
        "total_found": len(required_files) - len(missing)
    }


def check_agents() -> Dict[str, Any]:
    """
    Check agent registry and agent folders.
    
    Returns:
        Dict with agent system status
    """
    registry_path = PROJECT_ROOT / "agents" / "_registry.json"
    
    if not registry_path.exists():
        return {
            "status": "not_initialized",
            "registry_exists": False,
            "agent_count": 0
        }
    
    try:
        registry_data = json.loads(registry_path.read_text(encoding="utf-8"))
        agents = registry_data.get("agents", [])
        
        # Verify agent folders exist
        missing_folders = []
        for agent in agents:
            agent_path = PROJECT_ROOT / agent["path"]
            if not agent_path.exists():
                missing_folders.append(agent["agent_id"])
        
        return {
            "status": "healthy" if not missing_folders else "degraded",
            "registry_exists": True,
            "agent_count": len(agents),
            "missing_folders": missing_folders
        }
    except Exception as e:
        return {
            "status": "error",
            "registry_exists": True,
            "error": str(e)
        }


def check_logs() -> Dict[str, Any]:
    """
    Check log file status and sizes.
    
    Returns:
        Dict with log system status
    """
    log_dir = PROJECT_ROOT / ".tmp" / "logs"
    
    if not log_dir.exists():
        return {
            "status": "not_initialized",
            "log_count": 0
        }
    
    log_files = list(log_dir.glob("*.log"))
    
    log_info = []
    for log_file in log_files:
        size_kb = log_file.stat().st_size / 1024
        line_count = len(log_file.read_text(encoding="utf-8").splitlines())
        
        log_info.append({
            "name": log_file.name,
            "size_kb": round(size_kb, 2),
            "lines": line_count
        })
    
    return {
        "status": "healthy",
        "log_count": len(log_files),
        "logs": log_info
    }


def run_full_diagnostic() -> Dict[str, Any]:
    """
    Run complete system diagnostic.
    
    Returns:
        Comprehensive diagnostic report
    """
    info("Running full system diagnostic", service="system")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "directory_structure": check_directory_structure(),
        "core_files": check_core_files(),
        "agents": check_agents(),
        "logs": check_logs()
    }
    
    # Determine overall health
    statuses = [
        report["directory_structure"]["status"],
        report["core_files"]["status"],
        report["agents"]["status"],
        report["logs"]["status"]
    ]
    
    if all(s == "healthy" for s in statuses):
        report["overall_status"] = "healthy"
    elif any(s == "error" for s in statuses):
        report["overall_status"] = "error"
    elif any(s == "degraded" for s in statuses):
        report["overall_status"] = "degraded"
    else:
        report["overall_status"] = "not_initialized"
    
    return report


def print_diagnostic_report(report: Dict[str, Any]) -> None:
    """Pretty print diagnostic report to console."""
    from logger import LIME_GREEN, WHITE, RESET
    
    print(f"\n{LIME_GREEN}╔══════════════════════════════════════╗{RESET}")
    print(f"{LIME_GREEN}║{WHITE}   OMNI-NEXUS SYSTEM DIAGNOSTICS   {LIME_GREEN}║{RESET}")
    print(f"{LIME_GREEN}╚══════════════════════════════════════╝{RESET}\n")
    
    print(f"{WHITE}Overall Status: {LIME_GREEN}{report['overall_status'].upper()}{RESET}\n")
    
    # Directory structure
    dirs = report["directory_structure"]
    print(f"{WHITE}Directory Structure: {dirs['total_found']}/{dirs['total_required']}{RESET}")
    if dirs["missing_directories"]:
        print(f"  {WHITE}Missing: {', '.join(dirs['missing_directories'])}{RESET}")
    
    # Core files
    files = report["core_files"]
    print(f"{WHITE}Core Files: {files['total_found']}/{files['total_required']}{RESET}")
    if files["missing_files"]:
        print(f"  {WHITE}Missing: {', '.join(files['missing_files'])}{RESET}")
    
    # Agents
    agents = report["agents"]
    print(f"{WHITE}Agents: {agents.get('agent_count', 0)} registered{RESET}")
    if agents.get("missing_folders"):
        print(f"  {WHITE}Missing folders: {', '.join(agents['missing_folders'])}{RESET}")
    
    # Logs
    logs = report["logs"]
    print(f"{WHITE}Log Files: {logs['log_count']} active{RESET}")
    
    print()


if __name__ == "__main__":
    report = run_full_diagnostic()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_diagnostic_report(report)
