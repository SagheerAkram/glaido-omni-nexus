# Agent Specifications

> **Purpose**: Define agent type taxonomy and capabilities  
> **Derived From**: North Star (multi-agent orchestration) + Integrations (offline-only)  
> **Status**: Blueprint Phase

---

## Agent Taxonomy

### Core Agent Types

Omni-Nexus defines **four core agent types** for orchestration:

1. **Discovery Agents** — Find and catalog resources
2. **Execution Agents** — Perform computation and transformation
3. **Monitoring Agents** — Validate and observe system state
4. **Custom Agents** — User-defined specialized behaviors

---

## 1. Discovery Agents

### Purpose
Locate, identify, and catalog data sources, files, or system resources.

### Capabilities
- File system traversal
- Pattern matching (glob, regex)
- Metadata extraction
- Resource cataloging
- Index building

### Example Use Cases
- Index all JSON files in workspace
- Find agents matching specific type
- Catalog available tools
- Build dependency graph

### Input Schema
```json
{
  "task_id": "discovery_001",
  "search_pattern": "*.json",
  "search_root": "/path/to/search",
  "filters": {
    "min_size": 1024,
    "max_depth": 5
  }
}
```

### Output Schema
```json
{
  "task_id": "discovery_001",
  "status": "success",
  "discovered_items": [
    {
      "path": "/path/to/file.json",
      "type": "file",
      "size_bytes": 2048,
      "metadata": {}
    }
  ],
  "total_found": 1
}
```

---

## 2. Execution Agents

### Purpose
Transform data, execute computations, perform operations.

### Capabilities
- Data transformation
- File manipulation
- Algorithm execution
- Batch processing
- Result aggregation

### Example Use Cases
- Process JSON files into markdown reports
- Execute data validation pipeline
- Transform log files into structured data
- Run batch file operations

### Input Schema
```json
{
  "task_id": "execution_001",
  "operation_type": "transform",
  "input_data": {
    "source_files": ["/path/to/input.json"],
    "transform_type": "json_to_markdown"
  },
  "output_config": {
    "destination": "/path/to/output.md"
  }
}
```

### Output Schema
```json
{
  "task_id": "execution_001",
  "status": "success",
  "output_data": {
    "files_processed": 1,
    "output_files": ["/path/to/output.md"],
    "duration_ms": 1234
  }
}
```

---

## 3. Monitoring Agents

### Purpose
Validate system state, check health, verify correctness.

### Capabilities
- File integrity checks
- Schema validation
- System diagnostics
- Performance monitoring
- Anomaly detection

### Example Use Cases
- Verify all agents are responsive
- Check file integrity across workspace
- Monitor log file growth
- Validate registry consistency

### Input Schema
```json
{
  "task_id": "monitoring_001",
  "monitor_type": "health_check",
  "targets": ["agents", "tools", "logs"],
  "thresholds": {
    "max_log_size_mb": 100,
    "max_agent_count": 50
  }
}
```

### Output Schema
```json
{
  "task_id": "monitoring_001",
  "status": "success",
  "health_report": {
    "agents": {"status": "healthy", "count": 3},
    "tools": {"status": "healthy", "count": 10},
    "logs": {"status": "warning", "size_mb": 95}
  }
}
```

---

## 4. Custom Agents

### Purpose
User-defined agents for specialized workflows.

### Capabilities
- **User-defined** — No predefined constraints
- Must follow agent contract (input/output schemas)
- Can invoke any tool from tools/ layer
- Can coordinate with other agents

### Example Use Cases
- Domain-specific data processing
- Integration with custom file formats
- Specialized validation logic
- Custom reporting workflows

### Contract Requirements
All custom agents must:
1. Accept standardized input schema
2. Return standardized output schema
3. Log all operations
4. Handle errors gracefully
5. Never perform network I/O (offline constraint)

---

## Agent Lifecycle

### Spawn

```
1. User/CLI triggers agent spawn
2. Config validated against agent_config schema
3. Agent folder structure created
4. config.json, manifest.md, behavior.py generated
5. Agent registered in _registry.json
6. Status set to "active"
```

---

### Execution

```
1. Navigation receives task for agent
2. Agent loaded from agents/<agent_id>/behavior.py
3. execute(task_data) function called
4. Agent performs work via tools/ layer
5. Agent returns result payload
6. Result logged and returned to caller
```

---

### Termination

```
1. Agent marked as "inactive" in registry
2. Agent folder preserved (not deleted)
3. Future tasks no longer routed to agent
4. Agent can be reactivated or removed
```

---

## Agent Coordination

### Sequential Workflow

```
Task → Agent A → Output A
     → Agent B (uses Output A) → Output B
     → Agent C (uses Output B) → Final Result
```

**Orchestrated By**: Navigation/workflow_manager

---

### Parallel Workflow

```
Task → Agent A → Output A ↘
    → Agent B → Output B  → Aggregator → Final Result
    → Agent C → Output C ↗
```

**Orchestrated By**: Navigation/workflow_manager

---

## Agent Constraints

### Offline-First

- ❌ No external API calls
- ❌ No network requests
- ❌ No cloud service dependencies
- ✅ Local file system only
- ✅ In-memory computation
- ✅ Tool delegation

### No Heavy Logic

Per A.N.T. architecture:
- Agents are **orchestrators**, not executors
- Complex logic delegated to tools/ layer
- Agents coordinate, tools compute

### Stateless Execution

- Each agent invocation is independent
- No persistent state between invocations
- State stored in files, not in-memory

---

## Agent Directory Structure

```
agents/<agent_id>/
├── config.json          # Agent metadata
├── manifest.md          # Documentation
├── behavior.py          # Execution logic
└── tests/               # Optional test suite
    └── test_behavior.py
```

### config.json Schema

```json
{
  "agent_id": "agent_<name>",
  "name": "Human Readable Name",
  "type": "discovery|execution|monitoring|custom",
  "capabilities": ["capability1", "capability2"],
  "dependencies": ["tool1", "tool2"],
  "created_at": "ISO8601 timestamp",
  "version": "1.0.0"
}
```

---

## Agent Naming Conventions

### Agent ID Pattern

`agent_<descriptive_name>`

**Examples**:
- `agent_discovery`
- `agent_json_validator`
- `agent_report_generator`

**Rules**:
- Lowercase only
- Underscores for spaces
- Descriptive, not generic

---

## Agent Capability Vocabulary

**Standard Capabilities**:
- `file_search` — Search file system
- `data_transform` — Transform data formats
- `validation` — Validate schemas/integrity
- `aggregation` — Combine multiple sources
- `reporting` — Generate reports
- `monitoring` — Health checks
- `orchestration` — Coordinate other agents

Agents can define custom capabilities beyond this list.

---

## Summary

Agent specifications ensure:
- **Clear Taxonomy**: Four well-defined types
- **Consistent Interface**: Standardized input/output
- **Offline Operation**: No external dependencies
- **Layered Architecture**: Delegation to tools/
- **Extensibility**: Custom agents for domain needs
