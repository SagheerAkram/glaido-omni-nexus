"""
Tool: Schema Validator
Purpose: Validate JSON data against schemas defined in gemini.md
Category: core
Created: 2026-02-13T21:04:24+05:00
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, Tuple

# Add utilities to path
sys.path.append(str(Path(__file__).parent.parent / "utilities"))
from logger import error, success, info


def validate_agent_config(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate agent configuration against schema.
    
    Schema from gemini.md:
    {
      "agent_id": "agent_[lowercase]",
      "name": "Human Readable",
      "type": "discovery|execution|monitoring|custom",
      "capabilities": ["cap1", "cap2"],
      "dependencies": ["tool1", "tool2"]
    }
    
    Args:
        data: Agent config dictionary to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ["agent_id", "name", "type", "capabilities"]
    
    # Check required fields
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Validate agent_id pattern
    agent_id = data["agent_id"]
    if not agent_id.startswith("agent_"):
        return False, "agent_id must start with 'agent_'"
    
    if not agent_id[6:].replace("_", "").isalnum():
        return False, "agent_id must be lowercase alphanumeric with underscores"
    
    # Validate type
    valid_types = ["discovery", "execution", "monitoring", "custom"]
    if data["type"] not in valid_types:
        return False, f"type must be one of: {', '.join(valid_types)}"
    
    # Validate capabilities is list
    if not isinstance(data["capabilities"], list):
        return False, "capabilities must be an array"
    
    # Validate dependencies if present
    if "dependencies" in data and not isinstance(data["dependencies"], list):
        return False, "dependencies must be an array"
    
    return True, ""


def validate_tool_execution(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate tool execution payload against schema.
    
    Schema from gemini.md:
    {
      "tool_id": "tool_[name]",
      "input_data": {...},
      "execution_context": {
        "session_id": "...",
        "agent_id": "...",
        "timestamp": "...",
        "priority": 0-10
      }
    }
    
    Args:
        data: Tool execution payload to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ["tool_id", "input_data", "execution_context"]
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Validate tool_id pattern
    if not data["tool_id"].startswith("tool_"):
        return False, "tool_id must start with 'tool_'"
    
    # Validate execution_context
    context = data["execution_context"]
    if not isinstance(context, dict):
        return False, "execution_context must be an object"
    
    # Validate priority if present
    if "priority" in context:
        priority = context["priority"]
        if not isinstance(priority, int) or not (0 <= priority <= 10):
            return False, "priority must be integer between 0 and 10"
    
    return True, ""


def validate_routing_decision(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate navigation routing decision against schema.
    
    Schema from gemini.md:
    {
      "task_id": "...",
      "route_type": "agent_spawn|tool_call|workflow_trigger|error_recovery",
      "target": "agent_id or tool_id",
      "payload": {...},
      "fallback": "..."
    }
    
    Args:
        data: Routing decision to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ["task_id", "route_type", "target"]
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Validate route_type
    valid_types = ["agent_spawn", "tool_call", "workflow_trigger", "error_recovery"]
    if data["route_type"] not in valid_types:
        return False, f"route_type must be one of: {', '.join(valid_types)}"
    
    # Validate payload if present
    if "payload" in data and not isinstance(data["payload"], dict):
        return False, "payload must be an object"
    
    return True, ""


def validate(data: Dict[str, Any], schema_type: str) -> Tuple[bool, str]:
    """
    Main validation entry point.
    
    Args:
        data: Data to validate
        schema_type: Schema name (agent_config, tool_execution, routing_decision)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    validators = {
        "agent_config": validate_agent_config,
        "tool_execution": validate_tool_execution,
        "routing_decision": validate_routing_decision
    }
    
    if schema_type not in validators:
        return False, f"Unknown schema type: {schema_type}"
    
    return validators[schema_type](data)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python validator.py <schema_type> <json_data>")
        print("Schema types: agent_config, tool_execution, routing_decision")
        sys.exit(1)
    
    schema_type = sys.argv[1]
    json_data = json.loads(sys.argv[2])
    
    is_valid, error_msg = validate(json_data, schema_type)
    
    if is_valid:
        success(f"Validation passed for {schema_type}")
        print(json.dumps({"status": "valid"}, sort_keys=True))
    else:
        error(f"Validation failed: {error_msg}")
        print(json.dumps({"status": "invalid", "error": error_msg}, sort_keys=True))
        sys.exit(1)
