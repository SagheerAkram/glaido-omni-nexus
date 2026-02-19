"""
CLI Main Entry Point
Purpose: Command-line interface for Omni-Nexus
Category: cli
Created: 2026-02-13T21:06:00+05:00
"""

import sys
import io

# Configure UTF-8 for Windows console (must be before other imports)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
from pathlib import Path
import argparse
import subprocess

# Add modules to path
CLI_PATH = Path(__file__).parent
TOOLS_PATH = CLI_PATH.parent / "tools"
NAV_PATH = CLI_PATH.parent / "navigation"

sys.path.append(str(CLI_PATH / "display"))
sys.path.append(str(TOOLS_PATH / "utilities"))
sys.path.append(str(TOOLS_PATH / "core"))
sys.path.append(str(TOOLS_PATH / "agents"))
sys.path.append(str(NAV_PATH / "routing"))

from formatter import banner, header, separator, bullet, status_icon, color, box
from logger import info, success, error
import diagnostics
import agent_spawner
import registry
import task_router

# Import verification components
sys.path.insert(0, str(CLI_PATH / "display"))
import verification_renderer


def cmd_init(args):
    """Initialize Omni-Nexus system."""
    print(banner())
    print(header("SYSTEM INITIALIZATION"))
    print(separator())
    
    info("Running system diagnostics...", service="cli")
    report = diagnostics.run_full_diagnostic()
    
    if report["overall_status"] == "healthy":
        print(f"{status_icon('success')} {color('System structure verified', 'white')}")
    else:
        print(f"{status_icon('warning')} {color('System requires setup', 'white')}")
    
    print()
    success("Omni-Nexus initialized successfully", service="cli")


def cmd_status(args):
    """Show system status."""
    print(header("OMNI-NEXUS STATUS"))
    print(separator())
    
    # Run diagnostics
    report = diagnostics.run_full_diagnostic()
    
    # Directory structure
    dirs = report["directory_structure"]
    print(bullet(f"Directory Structure: {dirs['total_found']}/{dirs['total_required']}"))
    
    # Core files
    files = report["core_files"]
    print(bullet(f"Core Files: {files['total_found']}/{files['total_required']}"))
    
    # Agents
    agents_data = report["agents"]
    agent_count = agents_data.get("agent_count", 0)
    print(bullet(f"Active Agents: {agent_count}"))
    
    # Logs
    logs = report["logs"]
    print(bullet(f"Log Files: {logs['log_count']}"))
    
    print()
    print(f"Overall Status: {color(report['overall_status'].upper(), 'lime', bold=True)}")


def cmd_agent(args):
    """Agent management commands."""
    if args.agent_command == "list":
        agents = registry.list_agents()
        
        print(header("REGISTERED AGENTS"))
        print(separator())
        
        if not agents:
            print(color("No agents registered yet", "white"))
        else:
            for agent in agents:
                print(bullet(f"{agent['name']} ({agent['agent_id']}) - {agent['type']}"))
        print()
    
    elif args.agent_command == "spawn":
        if not args.config:
            error("--config argument required for spawn command", service="cli")
            return
        
        try:
            agent_config = json.loads(args.config)
            
            print(header("SPAWNING AGENT"))
            print(separator())
            print(bullet(f"Agent ID: {agent_config['agent_id']}"))
            print(bullet(f"Name: {agent_config['name']}"))
            print(bullet(f"Type: {agent_config['type']}"))
            print()
            
            if agent_spawner.spawn_agent(agent_config):
                print(f"{status_icon('success')} {color('Agent spawned successfully', 'white')}")
            else:
                print(f"{status_icon('error')} {color('Agent spawn failed', 'white')}")
        
        except json.JSONDecodeError:
            error("Invalid JSON config", service="cli")


def cmd_diagnostic(args):
    """Run system diagnostics."""
    print(header("RUNNING DIAGNOSTICS"))
    print(separator())
    
    report = diagnostics.run_full_diagnostic()
    
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        diagnostics.print_diagnostic_report(report)


def cmd_route(args):
    """Test task routing."""
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # DORMANT EXECUTION GUARD — Phase 6.4 Dormant State
    # Navigation routing is sealed until Expansion Gate unlock.
    # DO NOT remove this guard without completing the full
    # Expansion B.L.A.S.T. cycle and user approval.
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print("[!] ROUTE COMMAND DISABLED — SYSTEM IN DORMANT STATE")
    print("    Navigation routing remains sealed until Expansion Gate unlock.")
    return 0
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    if not args.task:  # noqa: unreachable — preserved for expansion activation
        error("--task argument required", service="cli")
        return
    
    try:
        task_data = json.loads(args.task)
        
        print(header("TASK ROUTING"))
        print(separator())
        print(bullet(f"Task ID: {task_data.get('task_id', 'unknown')}"))
        print(bullet(f"Task Type: {task_data.get('task_type', 'unknown')}"))
        print()
        
        decision = task_router.route_task(task_data)
        
        print(color("Routing Decision:", "lime", bold=True))
        print(json.dumps(decision, indent=2))
    
    except json.JSONDecodeError:
        error("Invalid JSON task data", service="cli")


def cmd_verify(args):
    """Run system verification."""
    # Get workspace root
    workspace = Path(__file__).resolve().parents[1]
    orchestrator_path = workspace / "navigation" / "orchestrator" / "verification_orchestrator.py"
    
    if not orchestrator_path.exists():
        error(f"Orchestrator not found: {orchestrator_path}", service="cli")
        return
    
    try:
        # Run verification orchestrator
        result = subprocess.run(
            [sys.executable, str(orchestrator_path)],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # Parse JSON output
        try:
            verification_data = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            error(f"Failed to parse orchestrator output: {e}", service="cli")
            if result.stdout:
                print("Raw output:")
                print(result.stdout)
            if result.stderr:
                print("Errors:")
                print(result.stderr)
            return
        
        # Render results using display contract
        output = verification_renderer.render_verification_results(verification_data)
        print(output)
        
        # Exit with orchestrator status
        sys.exit(result.returncode)
        
    except subprocess.TimeoutExpired:
        error("Verification timeout (exceeded 120 seconds)", service="cli")
        sys.exit(1)
    except Exception as e:
        error(f"Verification failed: {e}", service="cli")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Glaido Omni-Nexus - Autonomous AI Infrastructure",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # init command
    parser_init = subparsers.add_parser("init", help="Initialize system")
    parser_init.set_defaults(func=cmd_init)
    
    # status command
    parser_status = subparsers.add_parser("status", help="Show system status")
    parser_status.set_defaults(func=cmd_status)
    
    # agent command
    parser_agent = subparsers.add_parser("agent", help="Agent management")
    parser_agent.add_argument("agent_command", choices=["list", "spawn"], help="Agent subcommand")
    parser_agent.add_argument("--config", help="Agent config JSON (for spawn)")
    parser_agent.set_defaults(func=cmd_agent)
    
    # diagnostic command
    parser_diag = subparsers.add_parser("diagnostic", help="Run diagnostics")
    parser_diag.add_argument("--json", action="store_true", help="Output JSON")
    parser_diag.set_defaults(func=cmd_diagnostic)
    
    # route command
    parser_route = subparsers.add_parser("route", help="Test task routing")
    parser_route.add_argument("--task", required=True, help="Task JSON payload")
    parser_route.set_defaults(func=cmd_route)
    
    # verify command
    parser_verify = subparsers.add_parser("verify", help="Run system verification")
    parser_verify.set_defaults(func=cmd_verify)
    
    args = parser.parse_args()
    
    if not args.command:
        print(banner())
        parser.print_help()
        return
    
    # Execute command
    args.func(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{color('Operation cancelled', 'white')}")
        sys.exit(0)
    except Exception as e:
        error(f"Fatal error: {e}", service="cli")
        sys.exit(1)
