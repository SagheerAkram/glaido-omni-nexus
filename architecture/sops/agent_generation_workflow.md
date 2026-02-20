# Agent Generation Workflow — SOP

> **Purpose**: Define the complete lifecycle for spawning new autonomous agents  
> **Layer**: Architecture (SOP)  
> **Updated**: 2026-02-13T20:58:39+05:00

---

## 🎯 OVERVIEW

This SOP defines how Omni-Nexus autonomously generates, registers, and manages CLI agents.

### Workflow Stages
1. **Request Validation** → Validate agent specification against schema
2. **Folder Creation** → Generate agent directory structure
3. **File Generation** → Create config.json, manifest.md, behavior.py
4. **Registry Update** → Register agent in `agents/_registry.json`
5. **Verification** → Validate agent structure and dependencies
6. **Activation** → Make agent available to navigation orchestrator

---

## 📋 STAGE 1: REQUEST VALIDATION

### Input Schema
Agent creation requests must conform to `gemini.md` → `agent_config` schema:

```json
{
  "agent_id": "agent_[lowercase_name]",
  "name": "Human Readable Name",
  "type": "discovery|execution|monitoring|custom",
  "capabilities": ["capability1", "capability2"],
  "dependencies": ["tool_id1", "tool_id2"]
}
```

### Tool Responsible
`tools/agents/agent_spawner.py`

### Validation Rules
- ✅ `agent_id` must follow pattern `^agent_[a-z0-9_]+$`
- ✅ `type` must be one of: `discovery`, `execution`, `monitoring`, `custom`
- ✅ All `dependencies` must exist in `tools/`
- ✅ `agent_id` must not already exist in `agents/_registry.json`

### Failure Handling
- **Invalid Schema**: Return error, log to `.tmp/logs/agents.log`, exit
- **Duplicate ID**: Return error with existing agent path
- **Missing Dependencies**: Return error with list of missing tools

---

## 📂 STAGE 2: FOLDER CREATION

### Directory Structure
```
agents/
└── [agent_id]/
    ├── config.json
    ├── manifest.md
    └── behavior.py
```

### Tool Responsible
`tools/agents/agent_spawner.py`

### Actions
1. Create `agents/[agent_id]/` directory
2. Initialize empty files (populated in Stage 3)

### Failure Handling
- **Permission Denied**: Log error, suggest running with elevated permissions
- **Disk Full**: Log error, trigger cleanup of `.tmp/` if needed

---

## 📝 STAGE 3: FILE GENERATION

### config.json Template
```json
{
  "agent_id": "[from input]",
  "name": "[from input]",
  "type": "[from input]",
  "capabilities": [from input],
  "dependencies": [from input],
  "created_at": "[ISO 8601 timestamp]",
  "status": "active",
  "metadata": {
    "generated_by": "agent_spawner.py",
    "version": "1.0.0"
  }
}
```

### manifest.md Template
````markdown
# [Agent Name]

**Agent ID**: `[agent_id]`  
**Type**: [type]  
**Status**: Active  
**Created**: [timestamp]

## Capabilities
- [capability 1]
- [capability 2]

## Dependencies
- [dependency 1]
- [dependency 2]

## Behavior
See `behavior.py` for executable logic.
````

### behavior.py Template
```python
"""
Agent: [name]
ID: [agent_id]
Type: [type]
Generated: [timestamp]
"""

import sys
import json
from pathlib import Path

# Add tools to path
sys.path.append(str(Path(__file__).parent.parent.parent / "tools"))

class [CamelCaseAgentName]:
    def __init__(self):
        self.agent_id = "[agent_id]"
        self.capabilities = [capabilities as list]
        
    def execute(self, input_data: dict) -> dict:
        """
        Main execution entry point.
        
        Args:
            input_data: Dictionary matching navigation routing schema
            
        Returns:
            Dictionary with execution results
        """
        # TODO: Implement agent logic
        return {
            "status": "success",
            "agent_id": self.agent_id,
            "result": None
        }

if __name__ == "__main__":
    agent = [CamelCaseAgentName]()
    # CLI entry point for direct testing
    print(json.dumps(agent.execute({}), indent=2))
```

## Tool Responsible
`tools/agents/agent_spawner.py`

---

## 📋 STAGE 4: REGISTRY UPDATE

### Registry Location
`agents/_registry.json`

### Registry Schema
```json
{
  "agents": [
    {
      "agent_id": "agent_example",
      "name": "Example Agent",
      "type": "discovery",
      "path": "agents/agent_example",
      "status": "active",
      "created_at": "2026-02-13T20:58:39+05:00"
    }
  ],
  "last_updated": "2026-02-13T20:58:39+05:00"
}
```

### Actions
1. Load `agents/_registry.json`
2. Append new agent entry
3. Update `last_updated` timestamp
4. Write back to file

### Atomic Write
- Write to `.tmp/_registry.json.tmp`
- Validate JSON structure
- Atomic move to `agents/_registry.json`

---

## ✅ STAGE 5: VERIFICATION

### Checks
1. ✅ Agent folder exists
2. ✅ `config.json` is valid JSON and matches schema
3. ✅ `manifest.md` exists
4. ✅ `behavior.py` is syntactically valid Python
5. ✅ Agent registered in `_registry.json`

### Tool Responsible
`tools/agents/agent_spawner.py` (internal verification step)

### Failure Handling
- **Verification Failed**: Delete agent folder, rollback registry, return error

---

## 🚀 STAGE 6: ACTIVATION

### Navigation Layer Integration
- Navigation orchestrator reads `agents/_registry.json` on startup
- Agent becomes available for routing decisions
- Can be invoked via `navigation/agent_coordinator.py`

### CLI Access
- Agent can be tested directly: `python agents/[agent_id]/behavior.py`
- CLI commands can spawn agent: `python cli/main.py agent create --spec=spec.json`

---

## 🔄 SELF-ANNEALING INTEGRATION

### Failure Triggers
- Schema validation failure → Update schema in `gemini.md` if genuinely needed
- File write failure → Check permissions, update SOP with troubleshooting steps
- Registry corruption → Implement registry repair tool

### SOP Updates
- All unique failures logged in `findings.md` → Self-Annealing Learnings
- This SOP updated with new edge cases
- Recovery procedures documented in `architecture/edge_cases/`

---

**Last Updated**: 2026-02-13T20:58:39+05:00  
**Status**: Active — ready for implementation in Phase 3 (Architect)
