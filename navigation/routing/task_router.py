"""
Navigation: Task Router
Purpose: Route incoming tasks to appropriate agents/tools
Category: navigation/routing
Created: 2026-02-13T21:06:00+05:00

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DORMANT MODULE NOTICE
Status:  NOT ACTIVE — Phase 6.4 Dormant State
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1] MODULE EXECUTION BLOCKED
    This module IS imported by cli/main.py and the `route`
    CLI command IS wired to call route_task(). However,
    execution is intentionally blocked at the CLI layer by
    a Dormant Execution Guard in cmd_route() that intercepts
    all calls before they reach this module and returns
    without invoking any routing logic.
    It was implemented during Phase 3 (Architect) as
    scaffolding for future expansion.

[2] CLI ROUTE COMMAND WIRED — EXECUTION BLOCKED DURING DORMANT STATE
    The `route` command in cli/main.py imports this module
    but is guarded by a dormant-state check that prevents
    actual invocation. The only active execution entry point
    is: navigation/orchestrator/verification_orchestrator.py
    Task routing remains sealed behind Expansion Gate approval
    (Invariant #12). This module remains present for future
    expansion cycles.

[3] MIGRATION REQUIRED BEFORE ACTIVATION
    The functions _determine_route_type() and _determine_target()
    contain conditional branching logic (if/elif chains and
    registry lookups) that exceeds the "thin orchestration"
    threshold defined in Invariant #2 (A.N.T. Layer Separation).
    Before this module is wired to the CLI:
        • Branching decision logic must be extracted and migrated
          to the tools/ layer (e.g., tools/core/routing_engine.py)
        • This module must be reduced to pure pass-through routing
        • Architecture SOP must be updated to reflect the new split
        • Full Expansion B.L.A.S.T. cycle must be completed

    Failure to perform this migration will violate Invariant #2.

DO NOT REMOVE THIS NOTICE until the above migration is complete
and the Expansion Gate has been explicitly unlocked by the user.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Add tools to path
TOOLS_PATH = Path(__file__).parent.parent.parent / "tools"
sys.path.append(str(TOOLS_PATH / "utilities"))
sys.path.append(str(TOOLS_PATH / "core"))
sys.path.append(str(TOOLS_PATH / "agents"))

from logger import info, error, warning
from validator import validate
import registry as agent_registry


class TaskRouter:
    """
    Routes tasks to appropriate execution targets.
    
    Per navigation_routing.md SOP:
    - No heavy logic in navigation layer
    - Pure decision routing
    - Delegate execution to tools/agents
    """
    
    def __init__(self):
        """Initialize router with routing rules."""
        self.routing_rules = self._load_routing_rules()
    
    def _load_routing_rules(self) -> Dict[str, Any]:
        """
        Load routing decision rules.
        
        Returns:
            Routing rules configuration
        """
        # Default routing rules
        # In future, load from config/routing.json
        return {
            "task_types": {
                "agent_spawn": "tools/agents/agent_spawner.py",
                "diagnostic": "tools/core/diagnostics.py",
                "data_operation": "tools/data/file_ops.py",
                "validation": "tools/core/validator.py"
            },
            "fallback": "error_recovery"
        }
    
    def route(self, task_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route task to appropriate handler.
        
        Args:
            task_payload: Task data containing task_id, task_type, and payload
            
        Returns:
            Routing decision dict
        """
        task_id = task_payload.get("task_id", "unknown")
        task_type = task_payload.get("task_type")
        
        info(f"Routing task {task_id} (type: {task_type})", service="navigation")
        
        # Validation
        if not task_type:
            error(f"Task {task_id} missing task_type", service="navigation")
            return self._error_route(task_id, "Missing task_type")
        
        # Determine route based on task type
        routing_decision = {
            "task_id": task_id,
            "route_type": self._determine_route_type(task_type),
            "target": self._determine_target(task_type),
            "payload": task_payload.get("payload", {}),
            "timestamp": datetime.now().isoformat()
        }
        
        # Fallback handling
        if not routing_decision["target"]:
            warning(f"No route found for task type: {task_type}", service="navigation")
            routing_decision["route_type"] = "error_recovery"
            routing_decision["fallback"] = "unknown_task_type"
        
        info(f"Task {task_id} routed to {routing_decision['target']}", service="navigation")
        return routing_decision
    
    def _determine_route_type(self, task_type: str) -> str:
        """
        Determine routing type based on task type.
        
        Args:
            task_type: Type of task
            
        Returns:
            Route type (agent_spawn, tool_call, workflow_trigger, error_recovery)
        """
        if task_type.startswith("agent_"):
            return "agent_spawn"
        elif task_type in ["diagnostic", "validation", "data_operation"]:
            return "tool_call"
        elif task_type == "workflow":
            return "workflow_trigger"
        else:
            return "error_recovery"
    
    def _determine_target(self, task_type: str) -> Optional[str]:
        """
        Determine execution target for task type.
        
        Args:
            task_type: Type of task
            
        Returns:
            Target agent_id or tool path
        """
        # Check if agent exists for this task
        agents = agent_registry.list_agents()
        for agent in agents:
            if agent["type"] == task_type:
                return agent["agent_id"]
        
        # Check routing rules for tool
        if task_type in self.routing_rules["task_types"]:
            return self.routing_rules["task_types"][task_type]
        
        return None
    
    def _error_route(self, task_id: str, error_reason: str) -> Dict[str, Any]:
        """
        Create error routing decision.
        
        Args:
            task_id: Task identifier
            error_reason: Reason for error
            
        Returns:
            Error routing decision
        """
        return {
            "task_id": task_id,
            "route_type": "error_recovery",
            "target": "error_handler",
            "error": error_reason,
            "timestamp": datetime.now().isoformat()
        }
    
    def validate_routing_decision(self, decision: Dict[str, Any]) -> bool:
        """
        Validate routing decision against schema.
        
        Args:
            decision: Routing decision dict
            
        Returns:
            True if valid
        """
        is_valid, error_msg = validate(decision, "routing_decision")
        if not is_valid:
            error(f"Invalid routing decision: {error_msg}", service="navigation")
            return False
        return True


def route_task(task_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function for routing a task.
    
    Args:
        task_payload: Task data
        
    Returns:
        Routing decision
    """
    router = TaskRouter()
    decision = router.route(task_payload)
    
    # Validate decision
    if not router.validate_routing_decision(decision):
        error("Routing decision validation failed", service="navigation")
    
    return decision


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python task_router.py '<task_json>'")
        print("Example:")
        print('  python task_router.py \'{"task_id": "task_001", "task_type": "diagnostic", "payload": {}}\'')
        sys.exit(1)
    
    try:
        task_data = json.loads(sys.argv[1])
        decision = route_task(task_data)
        print(json.dumps(decision, indent=2))
    except json.JSONDecodeError as e:
        error(f"Invalid JSON: {e}", service="navigation")
        sys.exit(1)
