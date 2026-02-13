# Data Schemas

> **Purpose**: Complete payload format definitions for all system interactions  
> **Derived From**: gemini.md (schema foundation) + North Star (orchestration data flow)  
> **Status**: Blueprint Phase

---

## Schema Validation Rules

All JSON payloads MUST conform to schemas defined here. Validation performed by `tools/core/validator.py`.

---

## 1. Agent Config Schema

**Used For**: Agent creation and registration

```json
{
  "agent_id": "agent_<lowercase_name>",
  "name": "Human Readable Name",
  "type": "discovery|execution|monitoring|custom",
  "capabilities": ["capability1", "capability2"],
  "dependencies": ["tool1", "tool2"],
  "description": "Optional agent purpose description",
  "created_at": "2026-02-13T21:18:00+05:00",
  "version": "1.0.0"
}
```

**Required Fields**: `agent_id`, `name`, `type`, `capabilities`  
**Optional Fields**: `dependencies`, `description`, `created_at`, `version`

**Constraints**:
- `agent_id` must start with `agent_`
- `type` must be one of: `discovery`, `execution`, `monitoring`, `custom`
- `capabilities` must be non-empty array

---

## 2. Tool Execution Schema

**Used For**: Tool invocation payloads

```json
{
  "tool_id": "tool_<name>",
  "input_data": {
    "param1": "value1",
    "param2": "value2"
  },
  "execution_context": {
    "session_id": "session_<id>",
    "agent_id": "agent_<name>",
    "timestamp": "2026-02-13T21:18:00+05:00",
    "priority": 5
  }
}
```

**Required Fields**: `tool_id`, `input_data`, `execution_context`

**Constraints**:
- `tool_id` must start with `tool_`
- `priority` must be integer 0-10 (0=lowest, 10=highest)

---

## 3. Routing Decision Schema

**Used For**: Navigation layer routing decisions

```json
{
  "task_id": "task_<id>",
  "route_type": "agent_spawn|tool_call|workflow_trigger|error_recovery",
  "target": "agent_id or tool_path",
  "payload": {
    "task_specific_data": "..."
  },
  "fallback": "fallback_target",
  "timestamp": "2026-02-13T21:18:00+05:00"
}
```

**Required Fields**: `task_id`, `route_type`, `target`  
**Optional Fields**: `payload`, `fallback`, `timestamp`

**Constraints**:
- `route_type` must be one of: `agent_spawn`, `tool_call`, `workflow_trigger`, `error_recovery`

---

## 4. System Event Schema

**Used For**: Logging and event tracking

```json
{
  "event_id": "evt_<uuid>",
  "timestamp": "2026-02-13T21:18:00+05:00",
  "event_type": "agent_spawned|tool_executed|error_occurred|workflow_started",
  "service": "system|agents|tools|navigation|cli",
  "level": "info|warning|error|critical",
  "message": "Human-readable description",
  "metadata": {
    "additional": "context"
  }
}
```

**Required Fields**: `event_id`, `timestamp`, `event_type`, `service`, `level`, `message`  
**Optional Fields**: `metadata`

---

## 5. Agent Task Input Schema

**Used For**: Tasks sent to agents

```json
{
  "task_id": "task_<id>",
  "agent_id": "agent_<name>",
  "task_type": "discovery|execution|monitoring|custom",
  "input_data": {
    "task_specific_parameters": "..."
  },
  "timeout_seconds": 60,
  "priority": 5
}
```

**Required Fields**: `task_id`, `agent_id`, `task_type`, `input_data`  
**Optional Fields**: `timeout_seconds`, `priority`

**Defaults**:
- `timeout_seconds`: 60
- `priority`: 5

---

## 6. Agent Task Output Schema

**Used For**: Results returned from agents

```json
{
  "task_id": "task_<id>",
  "status": "success|error|timeout",
  "output_data": {
    "result_specific_data": "..."
  },
  "error": "Error message if status=error",
  "duration_ms": 1234,
  "timestamp": "2026-02-13T21:18:00+05:00"
}
```

**Required Fields**: `task_id`, `status`, `output_data`  
**Optional Fields**: `error`, `duration_ms`, `timestamp`

**Constraints**:
- `status` must be one of: `success`, `error`, `timeout`
- `error` required if `status` is `error`

---

## 7. Agent Registry Entry Schema

**Used For**: `agents/_registry.json` entries

```json
{
  "agent_id": "agent_<name>",
  "name": "Human Readable Name",
  "type": "discovery|execution|monitoring|custom",
  "path": "agents/<agent_id>",
  "status": "active|inactive|recovering",
  "created_at": "2026-02-13T21:18:00+05:00",
  "last_used": "2026-02-13T21:18:00+05:00"
}
```

**Required Fields**: `agent_id`, `name`, `type`, `path`, `status`, `created_at`  
**Optional Fields**: `last_used`

---

## 8. Workflow Definition Schema

**Used For**: Multi-agent workflow specifications

```json
{
  "workflow_id": "workflow_<name>",
  "name": "Human Readable Name",
  "description": "Workflow purpose",
  "steps": [
    {
      "step_id": "step_1",
      "agent_id": "agent_discovery",
      "input_mapping": {"source": "workflow_input.field1"},
      "output_mapping": {"target": "step_1_output"}
    },
    {
      "step_id": "step_2",
      "agent_id": "agent_execution",
      "input_mapping": {"source": "step_1_output"},
      "output_mapping": {"target": "workflow_output"}
    }
  ],
  "coordination": "sequential|parallel"
}
```

**Required Fields**: `workflow_id`, `name`, `steps`, `coordination`  
**Optional Fields**: `description`

---

## 9. Diagnostic Report Schema

**Used For**: System health reports

```json
{
  "timestamp": "2026-02-13T21:18:00+05:00",
  "overall_status": "healthy|degraded|error|not_initialized",
  "directory_structure": {
    "status": "healthy|degraded",
    "total_required": 19,
    "total_found": 16,
    "missing_directories": ["dir1", "dir2"]
  },
  "core_files": {
    "status": "healthy|degraded",
    "total_required": 4,
    "total_found": 4,
    "missing_files": []
  },
  "agents": {
    "status": "healthy|degraded|error",
    "agent_count": 3,
    "registry_exists": true
  },
  "logs": {
    "status": "healthy",
    "log_count": 5,
    "logs": [
      {"name": "system.log", "size_kb": 12.5, "lines": 150}
    ]
  }
}
```

---

## 10. CLI Command Schema

**Used For**: Internal CLI argument parsing

```json
{
  "command": "init|status|agent|diagnostic|route|workflow",
  "subcommand": "list|spawn|run|...",
  "options": {
    "config": "{...}",
    "json": true,
    "verbose": false
  },
  "arguments": ["arg1", "arg2"]
}
```

**Required Fields**: `command`  
**Optional Fields**: `subcommand`, `options`, `arguments`

---

## Schema Versioning

All schemas include implicit version 1.0.

**Future Changes**:
- Backward-compatible additions allowed
- Breaking changes require new schema version
- Version tracked in schema_version field

---

## Validation Error Format

When schema validation fails:

```json
{
  "valid": false,
  "schema_type": "agent_config",
  "errors": [
    {
      "field": "agent_id",
      "error": "Missing required field"
    },
    {
      "field": "type",
      "error": "Must be one of: discovery, execution, monitoring, custom"
    }
  ]
}
```

---

## Offline Data Constraints

All schemas assume:
- **No URLs** — All paths are local file system
- **No API endpoints** — No external service references
- **No auth tokens** — No authentication fields
- **Timestamps in ISO8601** — Local timezone aware
- **No UUIDs from external services** — All IDs generated locally

---

## Summary

Data schemas ensure:
- **Type Safety**: Structured JSON validation
- **Consistency**: All components use same formats
- **Offline-First**: No external references
- **Versioning**: Backward compatibility tracking
- **Clear Documentation**: Every field documented
