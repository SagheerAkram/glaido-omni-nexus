"""
Tool: Agent Spawner
Purpose: Generate new agent modules following approved SOP workflow
Category: agents
Created: 2026-02-13T21:04:24+05:00
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Add utilities and core to path
sys.path.append(str(Path(__file__).parent.parent / "utilities"))
sys.path.append(str(Path(__file__).parent.parent / "core"))

from logger import info, success, error
from validator import validate
import registry

# Project root
PROJECT_ROOT = Path(__file__).parent.parent.parent


def generate_agent_structure(agent_id: str, agent_data: Dict[str, Any]) -> bool:
    """
    Create agent directory structure with required files.
    
    Per agent_generation_workflow.md SOP:
    1. Validate config against schema
    2. Create agent folder
    3. Generate config.json
    4. Generate manifest.md
    5. Generate behavior.py stub
    
    Args:
        agent_id: Agent identifier (agent_[name])
        agent_data: Agent configuration dict
        
    Returns:
        True if successful
    """
    # Step 1: Validate
    is_valid, error_msg = validate(agent_data, "agent_config")
    if not is_valid:
        error(f"Agent config validation failed: {error_msg}", service="agents")
        return False
    
    # Step 2: Create folder
    agent_dir = PROJECT_ROOT / "agents" / agent_id
    if agent_dir.exists():
        error(f"Agent directory already exists: {agent_id}", service="agents")
        return False
    
    agent_dir.mkdir(parents=True, exist_ok=True)
    info(f"Created agent directory: {agent_id}", service="agents")
    
    # Step 3: Generate config.json
    config_path = agent_dir / "config.json"
    config_data = {
        "agent_id": agent_data["agent_id"],
        "name": agent_data["name"],
        "type": agent_data["type"],
        "capabilities": agent_data["capabilities"],
        "dependencies": agent_data.get("dependencies", []),
        "created_at": datetime.now().isoformat(),
        "version": "1.0.0"
    }
    
    config_path.write_text(json.dumps(config_data, indent=2), encoding="utf-8")
    info(f"Generated config.json for {agent_id}", service="agents")
    
    # Step 4: Generate manifest.md
    manifest_path = agent_dir / "manifest.md"
    manifest_content = f"""# {agent_data['name']}

> **Agent ID**: `{agent_id}`  
> **Type**: {agent_data['type']}  
> **Created**: {datetime.now().strftime('%Y-%m-%d')}

---

## Purpose

{agent_data.get('description', 'Agent purpose description goes here.')}

---

## Capabilities

{chr(10).join(f'- {cap}' for cap in agent_data['capabilities'])}

---

## Dependencies

{chr(10).join(f'- `{dep}`' for dep in agent_data.get('dependencies', [])) if agent_data.get('dependencies') else 'None'}

---

## Behavioral Rules

- Follow A.N.T. architecture invariants
- Log all actions via tools/utilities/logger.py
- Never perform heavy computation directly
- Delegate to tools/ layer for execution

---

## Integration Points

### Input Schema
```json
{{
  "task_id": "...",
  "input_data": {{}}
}}
```

### Output Schema
```json
{{
  "task_id": "...",
  "status": "success|error",
  "output_data": {{}}
}}
```
"""
    
    manifest_path.write_text(manifest_content, encoding="utf-8")
    info(f"Generated manifest.md for {agent_id}", service="agents")
    
    # Step 5: Generate behavior.py stub
    behavior_path = agent_dir / "behavior.py"
    behavior_content = f'''"""
Agent: {agent_data['name']}
Type: {agent_data['type']}
Created: {datetime.now().isoformat()}
"""

import sys
import json
from pathlib import Path

# Add tools to path
TOOLS_PATH = Path(__file__).parent.parent.parent / "tools"
sys.path.append(str(TOOLS_PATH / "utilities"))
sys.path.append(str(TOOLS_PATH / "core"))

from logger import info, success, error


def execute(task_data: dict) -> dict:
    """
    Main execution entry point for {agent_data['name']}.
    
    Args:
        task_data: Task payload containing task_id and input_data
        
    Returns:
        Result payload with status and output_data
    """
    task_id = task_data.get("task_id", "unknown")
    info(f"Executing task {{task_id}}", service="{agent_id}")
    
    try:
        # Agent logic goes here
        # Delegate heavy work to tools/ layer
        
        result = {{
            "task_id": task_id,
            "status": "success",
            "output_data": {{
                "message": "Agent executed successfully"
            }}
        }}
        
        success(f"Task {{task_id}} completed", service="{agent_id}")
        return result
        
    except Exception as e:
        error(f"Task {{task_id}} failed: {{e}}", service="{agent_id}")
        return {{
            "task_id": task_id,
            "status": "error",
            "error": str(e)
        }}


if __name__ == "__main__":
    # CLI testing
    if len(sys.argv) > 1:
        test_task = {{
            "task_id": "test_001",
            "input_data": {{}}
        }}
        result = execute(test_task)
        print(json.dumps(result, indent=2))
    else:
        info("{agent_data['name']} behavior module loaded", service="{agent_id}")
'''
    
    behavior_path.write_text(behavior_content, encoding="utf-8")
    info(f"Generated behavior.py stub for {agent_id}", service="agents")
    
    return True


def spawn_agent(agent_data: Dict[str, Any]) -> bool:
    """
    Complete agent spawn workflow.
    
    1. Generate agent structure
    2. Register in _registry.json
    
    Args:
        agent_data: Agent configuration (must include agent_id, name, type, capabilities)
        
    Returns:
        True if successful
    """
    agent_id = agent_data["agent_id"]
    
    info(f"Spawning agent: {agent_id}", service="agents")
    
    # Generate structure
    if not generate_agent_structure(agent_id, agent_data):
        error(f"Failed to generate agent structure for {agent_id}", service="agents")
        return False
    
    # Register
    if not registry.add_agent(agent_data):
        error(f"Failed to register agent {agent_id}", service="agents")
        return False
    
    success(f"Agent {agent_id} spawned successfully", service="agents")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python agent_spawner.py '<agent_config_json>'")
        print("Example:")
        print('  python agent_spawner.py \'{"agent_id": "agent_test", "name": "Test Agent", "type": "custom", "capabilities": ["testing"]}\'')
        sys.exit(1)
    
    try:
        agent_config = json.loads(sys.argv[1])
        success_result = spawn_agent(agent_config)
        sys.exit(0 if success_result else 1)
    except json.JSONDecodeError as e:
        error(f"Invalid JSON: {e}", service="agents")
        sys.exit(1)
