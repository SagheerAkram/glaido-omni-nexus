"""
Tool: Agent Registry Handler
Purpose: Atomic operations on agents/_registry.json with validation
Category: agents
Created: 2026-02-13T21:04:24+05:00
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
import shutil

# Add utilities to path
sys.path.append(str(Path(__file__).parent.parent / "utilities"))
from logger import error, success, info, warning

# Registry path
REGISTRY_PATH = Path(__file__).parent.parent.parent / "agents" / "_registry.json"
TEMP_REGISTRY_PATH = Path(__file__).parent.parent.parent / ".tmp" / "_registry.json.tmp"


def _ensure_registry_exists() -> None:
    """Create empty registry if it doesn't exist."""
    if not REGISTRY_PATH.exists():
        REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        initial_data = {
            "agents": [],
            "last_updated": datetime.now().isoformat()
        }
        REGISTRY_PATH.write_text(json.dumps(initial_data, indent=2), encoding="utf-8")
        info("Created new agent registry", service="agents")


def read_registry() -> Dict[str, Any]:
    """
    Read the agent registry.
    
    Returns:
        Registry data dictionary
    """
    _ensure_registry_exists()
    
    try:
        data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        return data
    except json.JSONDecodeError as e:
        error(f"Registry corrupted: {e}", service="agents")
        raise


def write_registry(data: Dict[str, Any]) -> bool:
    """
    Atomically write registry data.
    
    Uses temp file + atomic move pattern for safety.
    
    Args:
        data: Registry data to write
        
    Returns:
        True if successful
    """
    try:
        # Update timestamp
        data["last_updated"] = datetime.now().isoformat()
        
        # Write to temp file first
        TEMP_REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        TEMP_REGISTRY_PATH.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8"
        )
        
        # Validate temp file is valid JSON
        json.loads(TEMP_REGISTRY_PATH.read_text(encoding="utf-8"))
        
        # Atomic move
        shutil.move(str(TEMP_REGISTRY_PATH), str(REGISTRY_PATH))
        
        return True
    except Exception as e:
        error(f"Failed to write registry: {e}", service="agents")
        if TEMP_REGISTRY_PATH.exists():
            TEMP_REGISTRY_PATH.unlink()
        return False


def agent_exists(agent_id: str) -> bool:
    """Check if agent ID exists in registry."""
    registry = read_registry()
    return any(agent["agent_id"] == agent_id for agent in registry["agents"])


def add_agent(agent_data: Dict[str, Any]) -> bool:
    """
    Add new agent to registry.
    
    Args:
        agent_data: Agent configuration dict
        
    Returns:
        True if successful
    """
    agent_id = agent_data["agent_id"]
    
    # Check for duplicates
    if agent_exists(agent_id):
        error(f"Agent '{agent_id}' already exists in registry", service="agents")
        return False
    
    # Add to registry
    registry = read_registry()
    
    registry_entry = {
        "agent_id": agent_id,
        "name": agent_data["name"],
        "type": agent_data["type"],
        "path": f"agents/{agent_id}",
        "status": "active",
        "created_at": datetime.now().isoformat()
    }
    
    registry["agents"].append(registry_entry)
    
    if write_registry(registry):
        success(f"Agent '{agent_id}' registered successfully", service="agents")
        return True
    
    return False


def remove_agent(agent_id: str) -> bool:
    """
    Remove agent from registry.
    
    Args:
        agent_id: Agent ID to remove
        
    Returns:
        True if successful
    """
    if not agent_exists(agent_id):
        warning(f"Agent '{agent_id}' not found in registry", service="agents")
        return False
    
    registry = read_registry()
    registry["agents"] = [
        agent for agent in registry["agents"]
        if agent["agent_id"] != agent_id
    ]
    
    if write_registry(registry):
        success(f"Agent '{agent_id}' removed from registry", service="agents")
        return True
    
    return False


def list_agents(agent_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List all agents, optionally filtered by type.
    
    Args:
        agent_type: Optional type filter (discovery, execution, monitoring, custom)
        
    Returns:
        List of agent entries
    """
    registry = read_registry()
    agents = registry["agents"]
    
    if agent_type:
        agents = [a for a in agents if a["type"] == agent_type]
    
    return agents


def get_agent(agent_id: str) -> Optional[Dict[str, Any]]:
    """
    Get specific agent details.
    
    Args:
        agent_id: Agent ID to retrieve
        
    Returns:
        Agent entry or None if not found
    """
    registry = read_registry()
    
    for agent in registry["agents"]:
        if agent["agent_id"] == agent_id:
            return agent
    
    return None


if __name__ == "__main__":
    # CLI testing
    if len(sys.argv) < 2:
        print("Usage: python registry.py <command> [args]")
        print("Commands: list, get <id>, exists <id>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list":
        agents = list_agents()
        print(json.dumps(agents, indent=2))
    elif command == "get" and len(sys.argv) > 2:
        agent = get_agent(sys.argv[2])
        print(json.dumps(agent, indent=2))
    elif command == "exists" and len(sys.argv) > 2:
        exists = agent_exists(sys.argv[2])
        print(json.dumps({"exists": exists}))
    else:
        error("Invalid command or missing arguments")
        sys.exit(1)
