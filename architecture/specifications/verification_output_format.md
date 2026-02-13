# Verification Output Format Specification

> **Purpose**: Define unified JSON structure returned by verification orchestrator  
> **Derived From**: Link Verification Protocol + Data Schemas  
> **Status**: Documentation Only — No Executable Logic

---

## Core Principle

All verification outputs must use a **standardized JSON format** to ensure consistency across the verification pipeline and maintain clear A.N.T. layer separation.

---

## Orchestrator Output Schema

### Top-Level Structure

```json
{
  "orchestrator": "verification_orchestrator",
  "timestamp": "2026-02-13T21:33:00+05:00",
  "overall_status": "ready|not_ready",
  "system_ready": true,
  "verifications": {
    "local_dependencies": { /* tool output */ },
    "filesystem_integrity": { /* tool output */ },
    "schema_validation": { /* tool output */ },
    "agent_registry": { /* tool output */ }
  },
  "execution_order": [
    "local_dependencies",
    "filesystem_integrity", 
    "schema_validation",
    "agent_registry"
  ]
}
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `orchestrator` | string | Yes | Identifies orchestrator type |
| `timestamp` | ISO8601 | Yes | Verification execution time (local) |
| `overall_status` | enum | Yes | `ready` or `not_ready` |
| `system_ready` | boolean | Yes | Final readiness flag for consumption |
| `verifications` | object | Yes | Individual tool results keyed by category |
| `execution_order` | array | Yes | Sequential order tools were executed |

---

## Individual Tool Output Schema

Each tool in the `verifications` object returns:

```json
{
  "category": "local_dependencies|filesystem_integrity|schema_validation|agent_registry",
  "status": "ready|healthy|not_ready|degraded|error",
  "executed": true,
  "exit_code": 0,
  "error": null,
  /* tool-specific fields */
}
```

### Common Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `category` | string | Yes | Tool category identifier |
| `status` | enum | Yes | Tool execution status |
| `executed` | boolean | Yes | Whether tool ran successfully |
| `exit_code` | integer | Yes | Process exit code (0=success) |
| `error` | string/null | No | Error message if tool failed |

---

## Tool-Specific Schemas

### 1. Local Dependencies Output

```json
{
  "category": "local_dependencies",
  "status": "ready|not_ready",
  "executed": true,
  "exit_code": 0,
  "python_version": {
    "current": "3.11.0",
    "required": "3.8",
    "meets_requirement": true
  },
  "modules": {
    "required": ["json", "pathlib", "sys", "shutil", "datetime", "argparse", "subprocess"],
    "available": ["json", "pathlib", "..."],
    "missing": [],
    "all_available": true
  },
  "filesystem": {
    "writable": true,
    "error": null
  }
}
```

---

### 2. Filesystem Integrity Output

```json
{
  "category": "filesystem_integrity",
  "status": "healthy|degraded|error",
  "executed": true,
  "exit_code": 0,
  "directories": {
    "required": 19,
    "found": 19,
    "missing": []
  },
  "core_files": {
    "required": 4,
    "found": 4,
    "missing": [],
    "unreadable": [],
    "empty": []
  },
  "architecture_immutable": true,
  "temp_writable": true
}
```

---

### 3. Schema Validation Output

```json
{
  "category": "schema_validation",
  "status": "ready|not_ready",
  "executed": true,
  "exit_code": 0,
  "validator_file": {
    "path": "tools/core/validator.py",
    "exists": true
  },
  "validator_import": {
    "importable": true,
    "has_validate_function": true,
    "error": null
  },
  "schema_documentation": {
    "exists": true,
    "documented_schemas": {
      "agent_config": true,
      "tool_execution": true,
      "routing_decision": true
    }
  }
}
```

---

### 4. Agent Registry Output

```json
{
  "category": "agent_registry",
  "status": "ready|not_ready",
  "executed": true,
  "exit_code": 0,
  "registry_exists": true,
  "registry_valid_json": true,
  "registry_valid_structure": true,
  "registry_writable": true,
  "backup_functional": true,
  "agent_count": 0,
  "errors": []
}
```

---

## Status Value Definitions

### Overall Status

| Value | Meaning |
|-------|---------|
| `ready` | All verifications passed, system operational |
| `not_ready` | One or more verifications failed |

### Tool-Specific Status

| Value | Meaning | Tools Using |
|-------|---------|-------------|
| `ready` | Tool checks passed | local_dependencies, schema_validation, agent_registry |
| `healthy` | All checks passed | filesystem_integrity |
| `degraded` | Non-critical issues detected | filesystem_integrity |
| `error` | Critical failure | filesystem_integrity |
| `not_ready` | Checks failed | All tools |

---

## A.N.T. Layer Separation

### Tools Layer (Layer 3)

**Responsibility**: Generate individual verification results

- Each tool outputs its own JSON structure
- Tool contains verification logic
- No knowledge of orchestrator

**Example**: `local_dependency_check.py` produces `local_dependencies` object

---

### Navigation Layer (Layer 2)

**Responsibility**: Aggregate tool results into unified format

- Orchestrator collects tool outputs
- Wraps in standard envelope
- Adds metadata (`timestamp`, `execution_order`)
- Determines `overall_status` (simple boolean logic only)

**Example**: `verification_orchestrator.py` wraps all tools in `verifications` object

---

### Architecture Layer (Layer 1)

**Responsibility**: Define output schemas

- Document expected formats (this specification)
- No execution logic
- Reference documentation only

**Example**: This file defines schemas, tools implement them

---

## Output Consumption

### CLI Layer

**Usage**: Pretty-print verification results

```python
# Conceptual CLI usage
result = run_orchestrator()
if result["system_ready"]:
    print_success("System Ready")
else:
    print_error("System Not Ready")
    print_details(result["verifications"])
```

### Diagnostic Tools

**Usage**: Check system health

```python
# Future diagnostic usage
status = verification_orchestrator.run()
if not status["system_ready"]:
    trigger_error_recovery(status["verifications"])
```

---

## Offline-First Constraints

### No External Dependencies

- ✅ All fields derived from local checks
- ✅ Timestamps use local timezone
- ✅ No network connectivity fields
- ✅ No external service status

### Deterministic Output

- ✅ Same system state = same output
- ✅ No randomness in status determination
- ✅ Reproducible verification results

---

## Schema Versioning

**Current Version**: 1.0

**Version Field** (future):
```json
{
  "schema_version": "1.0",
  "orchestrator": "verification_orchestrator",
  ...
}
```

**Compatibility**:
- Breaking changes require new major version
- Additive changes allowed in same version
- Tools must match orchestrator schema version

---

## Summary

Verification output format ensures:
- **Consistency**: All tools use standard structure
- **A.N.T. Separation**: Clear layer boundaries (tools → navigation → architecture)
- **Offline-First**: No external data dependencies
- **Determinism**: Reproducible results
- **Extensibility**: Additional tools can be added following same schema pattern
