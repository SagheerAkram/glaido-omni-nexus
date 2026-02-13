# Tool Lifecycle Management — SOP

> **Purpose**: Define creation, testing, deployment, and retirement of execution tools  
> **Layer**: Architecture (SOP)  
> **Updated**: 2026-02-13T20:58:39+05:00

---

## 🎯 OVERVIEW

Tools are **atomic, deterministic Python scripts** in Layer 3 that perform all system execution.

### Tool Characteristics
- ✅ Single responsibility (do one thing well)
- ✅ Deterministic (same input = same output)
- ✅ Schema-validated inputs/outputs
- ✅ File-based persistence (no external databases)
- ✅ Testable in isolation
- ✅ Offline-first (no network dependencies)

---

## 📂 TOOL STRUCTURE

### Directory Organization
```
tools/
├── core/          → System utilities (health, diagnostics, validation)
├── agents/        → Agent management (spawn, monitor, terminate)
├── data/          → Data operations (fetch, transform, load)
├── integrations/  → External adapters (disabled by default)
└── utilities/     → Helpers (logger, timer, sanitizer)
```

### Tool Template
```python
"""
Tool: [Tool Name]
Purpose: [Brief description]
Category: core|agents|data|integrations|utilities
Created: [ISO 8601 timestamp]
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any

# Schema definitions (validated against gemini.md)
INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "param1": {"type": "string"},
        # ...
    },
    "required": ["param1"]
}

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["success", "error"]},
        "result": {"type": "object"}
    },
    "required": ["status"]
}

def validate_input(data: Dict[str, Any]) -> bool:
    """Validate input against schema."""
    # Implementation validates against INPUT_SCHEMA
    pass

def execute(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main execution function.
    
    Args:
        input_data: Dictionary matching INPUT_SCHEMA
        
    Returns:
        Dictionary matching OUTPUT_SCHEMA
    """
    if not validate_input(input_data):
        return {
            "status": "error",
            "error": "Invalid input schema",
            "result": None
        }
    
    try:
        # Tool logic here
        result = perform_operation(input_data)
        
        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "result": None
        }

def perform_operation(data: Dict[str, Any]) -> Any:
    """Core tool logic."""
    # Deterministic execution
    pass

if __name__ == "__main__":
    # CLI entry point for direct testing
    if len(sys.argv) < 2:
        print("Usage: python tool.py <json_input>")
        sys.exit(1)
    
    input_json = json.loads(sys.argv[1])
    output = execute(input_json)
    print(json.dumps(output, indent=2))
```

---

## 🔄 TOOL LIFECYCLE STAGES

### Stage 1: Specification
**Document in**: `architecture/specifications/tool_specs.md`

**Required Info**:
- Tool name and ID
- Purpose and responsibility
- Input schema (JSON)
- Output schema (JSON)
- Dependencies (other tools, libraries)
- Error scenarios

### Stage 2: Implementation
**Location**: `tools/[category]/[tool_id].py`

**Requirements**:
- Follow template structure
- Implement schema validation
- Handle all error scenarios
- Return standardized output
- No external network calls (unless in `integrations/`)

### Stage 3: Testing
**Test Location**: `tests/unit/test_[tool_id].py`

**Test Coverage**:
- ✅ Valid input → expected output
- ✅ Invalid input → error response
- ✅ Edge cases (empty data, missing fields)
- ✅ Determinism (same input always same output)
- ✅ File persistence (if applicable)

**Test Template**:
```python
import pytest
import json
from tools.[category].[tool_id] import execute

def test_valid_input():
    input_data = {"param1": "value"}
    result = execute(input_data)
    assert result["status"] == "success"
    assert result["result"] is not None

def test_invalid_input():
    input_data = {}  # Missing required param
    result = execute(input_data)
    assert result["status"] == "error"
```

### Stage 4: Registration
**Update**: `architecture/specifications/tool_specs.md`

**Add Entry**:
```markdown
## [tool_id]
- **Category**: [category]
- **Purpose**: [description]
- **Input Schema**: `gemini.md → [schema_name]`
- **Output Schema**: `gemini.md → [schema_name]`
- **Status**: Active
- **Created**: [timestamp]
```

### Stage 5: Integration
**Navigation Integration**: Update routing rules to include new tool

**Agent Integration**: Agents can now declare dependency on this tool

### Stage 6: Monitoring
**Logs**: All executions logged to `.tmp/logs/tools.log`

**Metrics**:
- Execution count
- Success rate
- Average execution time
- Error frequency

### Stage 7: Retirement (if needed)
**Process**:
1. Check dependencies (agents using this tool)
2. Migrate dependents to replacement tool
3. Mark as deprecated in specs
4. After 30 days → move to `tools/deprecated/`

---

## 🛡️ TOOL DEVELOPMENT RULES

### Determinism
```python
# ✅ DETERMINISTIC
def transform_data(input_str):
    return input_str.upper()

# ❌ NON-DETERMINISTIC
def transform_data(input_str):
    return f"{input_str}_{random.randint(1, 100)}"  # ❌ Random output
```

### File-Based Persistence
```python
# ✅ CORRECT
def save_data(data):
    path = Path(".tmp/data.json")
    path.write_text(json.dumps(data))
    return {"status": "success", "path": str(path)}

# ❌ FORBIDDEN
def save_data(data):
    db.insert(data)  # ❌ No external databases
```

### Offline-First
```python
# ✅ CORRECT
def get_config():
    return json.loads(Path("config/system.json").read_text())

# ❌ FORBIDDEN (unless in tools/integrations/)
def get_config():
    response = requests.get("https://api.example.com/config")  # ❌ Network call
```

---

## 🔄 SELF-ANNEALING INTEGRATION

### Tool Failure Triggers Repair
1. Tool returns error status
2. Navigation logs error → `.tmp/logs/system.log`
3. `tools/core/diagnostics.py` analyzes failure
4. Engineer patches tool
5. Update this SOP with new edge case
6. Add test case to prevent recurrence

---

**Last Updated**: 2026-02-13T20:58:39+05:00  
**Status**: SOP defined — ready for Phase 3 (Architect) implementation
