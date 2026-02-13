# Verification Execution Flow — SOP

> **Purpose**: Document linear end-to-end verification pipeline execution flow  
> **Derived From**: Link Verification Protocol + Baseline Orchestrator  
> **Status**: Documentation Only — Descriptive Specification

---

## Core Principle

The verification pipeline follows a **strictly linear, sequential execution model** with no branching, decision trees, or conditional routing. This ensures predictable, deterministic verification of system readiness.

---

## Execution Flow Overview

The verification pipeline consists of a single chain:

```
CLI (future trigger) 
  → verification_orchestrator 
    → 4 verification tools (sequential) 
      → unified JSON output
```

---

## Flow Stages

### Stage 1: CLI Trigger (Future)

**Component**: `cli/verify.py` (not yet implemented)

**Responsibility**:
- Receive user command: `glaido verify`
- Parse command-line arguments (none currently expected)
- Invoke orchestrator as subprocess
- Capture JSON output
- Format results for terminal display

**Current Status**: Not implemented — CLI layer frozen during Architect phase

**Future Behavior**:
```python
# Conceptual CLI implementation
def verify_command():
    result = subprocess.run(
        ["python", "navigation/orchestrator/verification_orchestrator.py"],
        capture_output=True
    )
    json_output = json.loads(result.stdout)
    display_verification_results(json_output)
```

---

### Stage 2: Orchestrator Invocation

**Component**: `navigation/orchestrator/verification_orchestrator.py`

**Responsibility**:
- Execute 4 verification tools in fixed sequential order
- Capture JSON output from each tool
- Aggregate results into unified report
- Determine overall system readiness status
- Return standardized JSON output

**Execution Model**: Linear subprocess invocation

**Key Characteristics**:
- No decision logic
- No conditional tool skipping
- No retry mechanisms
- No parallel execution
- No state persistence

**Process**:
1. Resolve workspace root path
2. Define tool paths in array (order fixed)
3. For each tool:
   - Spawn subprocess with Python interpreter
   - Set 30-second timeout
   - Capture stdout as JSON
   - Parse and store result
4. Aggregate all results
5. Compute `overall_status` (all-pass or any-fail)
6. Print unified JSON to stdout
7. Exit with status code (0=ready, 1=not_ready)

---

### Stage 3: Sequential Tool Execution

**Execution Order** (derived from Link Verification Protocol):

#### 3.1: Local Dependency Check

**Tool**: `tools/core/local_dependency_check.py`

**Checks**:
- Python version ≥ 3.8
- Required stdlib modules available
- Filesystem write permissions

**Output Schema**:
```json
{
  "category": "local_dependencies",
  "status": "ready|not_ready",
  "python_version": { /* version info */ },
  "modules": { /* module availability */ },
  "filesystem": { /* writability */ }
}
```

**Exit Behavior**: Prints JSON to stdout, exits with 0 (always, even if not ready)

---

#### 3.2: Filesystem Integrity Check

**Tool**: `tools/core/filesystem_integrity_check.py`

**Checks**:
- A.N.T. directory structure exists
- Core files readable (gemini.md, README.md, LICENSE, progress.md)
- Architecture layer immutability (conceptual check)
- Temp directory writable

**Output Schema**:
```json
{
  "category": "filesystem_integrity",
  "status": "healthy|degraded|error",
  "directories": { /* missing dirs */ },
  "core_files": { /* file checks */ },
  "architecture_immutable": true,
  "temp_writable": true
}
```

**Exit Behavior**: Prints JSON to stdout, exits with 0 (always)

---

#### 3.3: Schema Validator Stub

**Tool**: `tools/core/schema_validator_stub.py`

**Checks**:
- `tools/core/validator.py` exists
- Validator module is importable
- `validate()` function exists
- Schema documentation present

**Output Schema**:
```json
{
  "category": "schema_validation",
  "status": "ready|not_ready",
  "validator_file": { /* existence check */ },
  "validator_import": { /* import check */ },
  "schema_documentation": { /* docs check */ }
}
```

**Exit Behavior**: Prints JSON to stdout, exits with 0 (always)

---

#### 3.4: Agent Registry Readiness Check

**Tool**: `tools/agents/registry_readiness_check.py`

**Checks**:
- `agents/_registry.json` exists
- Registry is valid JSON
- Registry structure matches schema
- Registry writable
- Backup mechanism functional

**Output Schema**:
```json
{
  "category": "agent_registry",
  "status": "ready|not_ready",
  "registry_exists": true,
  "registry_valid_json": true,
  "registry_valid_structure": true,
  "registry_writable": true,
  "backup_functional": true,
  "agent_count": 0
}
```

**Exit Behavior**: Prints JSON to stdout, exits with 0 (always)

---

### Stage 4: Result Aggregation

**Component**: `verification_orchestrator.py` (aggregation logic)

**Aggregation Rules**:

1. **Execution Check**: All tools must execute successfully (no timeout/crash)
2. **Status Check**: All tools must return `ready` or `healthy` status
3. **Overall Status**:
   - If both checks pass → `overall_status = "ready"`
   - Otherwise → `overall_status = "not_ready"`

**No Complex Logic**: Simple boolean AND operation, no scoring or weighted evaluation

**Metadata Addition**:
- `orchestrator`: Identifies orchestrator type
- `timestamp`: Local execution time (ISO8601)
- `execution_order`: Array of tool categories in execution order

---

### Stage 5: Unified JSON Output

**Component**: `verification_orchestrator.py` (JSON serialization)

**Output Format** (defined in `verification_output_format.md`):

```json
{
  "orchestrator": "verification_orchestrator",
  "timestamp": "2026-02-13T21:35:00+05:00",
  "overall_status": "ready|not_ready",
  "system_ready": true,
  "verifications": {
    "local_dependencies": { /* tool 1 output */ },
    "filesystem_integrity": { /* tool 2 output */ },
    "schema_validation": { /* tool 3 output */ },
    "agent_registry": { /* tool 4 output */ }
  },
  "execution_order": [
    "local_dependencies",
    "filesystem_integrity",
    "schema_validation",
    "agent_registry"
  ]
}
```

**Serialization**: `json.dumps(report, indent=2)`

**Output Destination**: stdout (for parent process capture)

---

### Stage 6: CLI Display (Future)

**Component**: `cli/verify.py` (not yet implemented)

**Future Responsibilities**:
- Parse JSON from orchestrator stdout
- Apply ANSI color formatting (brand colors)
- Display overall status prominently
- Show individual tool results in structured format
- Exit with status code matching orchestrator

**Display Pattern** (conceptual):
```
╔════════════════════════════════════╗
║  SYSTEM VERIFICATION RESULTS       ║
╚════════════════════════════════════╝

Overall Status: ✅ READY

Local Dependencies:    ✅ ready
Filesystem Integrity:  ✅ healthy
Schema Validation:     ✅ ready
Agent Registry:        ✅ ready

System is operational.
```

---

## Data Flow Summary

### Input Data

**Orchestrator receives**: No arguments (stateless invocation)

**Tools receive**: No arguments (each determines own checks)

---

### Output Data

**Tools produce**: Individual JSON verification reports

**Orchestrator produces**: Aggregated JSON verification report

**CLI consumes** (future): Orchestrator JSON for display

---

## Execution Guarantees

### Linearity

- Tools execute in fixed order: 1 → 2 → 3 → 4
- No parallelization
- No conditional skipping
- No early termination

### Determinism

- Same system state → same output
- No randomness in execution
- No external data dependencies
- Reproducible results

### Isolation

- Each tool executes as independent subprocess
- No shared state between tools
- Tool failures don't crash orchestrator
- Clean separation of concerns

---

## Error Handling

### Tool Timeout

**Scenario**: Tool exceeds 30-second execution limit

**Orchestrator Behavior**:
- Catch `subprocess.TimeoutExpired`
- Generate error result: `{"status": "error", "executed": false, "error": "Tool execution timeout"}`
- Continue to next tool
- Include error in unified output

---

### Tool Crash

**Scenario**: Tool subprocess exits with non-zero code or crashes

**Orchestrator Behavior**:
- Capture exit code
- Include in result: `{"exit_code": X, "executed": true}`
- Continue to next tool
- Overall status becomes `not_ready`

---

### Invalid JSON Output

**Scenario**: Tool prints malformed JSON

**Orchestrator Behavior**:
- Catch `json.JSONDecodeError`
- Generate error result: `{"status": "error", "executed": false, "error": "Invalid JSON output: <message>"}`
- Continue to next tool
- Overall status becomes `not_ready`

---

### Orchestrator Crash

**Scenario**: Orchestrator itself crashes

**Future CLI Behavior**:
- Detect subprocess non-zero exit without JSON
- Display error: "Orchestrator failed to execute"
- Exit with error code

---

## A.N.T. Layer Mapping

### Tools Layer (Layer 3)

**Components**:
- `local_dependency_check.py`
- `filesystem_integrity_check.py`
- `schema_validator_stub.py`
- `registry_readiness_check.py`

**Responsibilities**:
- Perform actual verification logic
- Check system state
- Return structured results
- No orchestration awareness

---

### Navigation Layer (Layer 2)

**Component**:
- `verification_orchestrator.py`

**Responsibilities**:
- Sequential tool invocation
- Result aggregation
- Minimal status determination
- No business logic

---

### Architecture Layer (Layer 1)

**Components**:
- `link_verification_protocol.md` (defines verification strategy)
- `verification_output_format.md` (defines output schemas)
- `verification_execution_flow.md` (this document)

**Responsibilities**:
- Document execution flow
- Define data contracts
- Establish verification requirements

---

## Offline-First Constraints

### No External Dependencies

- All tools use local checks only
- No network requests
- No external service queries
- No API calls

### Local Filesystem Only

- Read local files
- Write to local temp directories
- No database connections
- No remote storage

### Deterministic Output

- Same filesystem state → same results
- No time-based randomness (timestamps are metadata only)
- Reproducible verification

---

## Extension Points (Post-Stylize)

### Future Enhancements (Blocked Until Approval)

**Possible expansions** (NOT YET IMPLEMENTED):

1. **Parallel Tool Execution**: Run tools concurrently for speed
2. **Conditional Skipping**: Skip non-critical tools if critical ones fail
3. **Retry Mechanisms**: Retry failed tools with exponential backoff
4. **Severity Levels**: Distinguish critical vs. warning-level failures
5. **Detailed Diagnostics**: Provide fix suggestions for failures
6. **Incremental Verification**: Skip unchanged components

**Current Rule**: Pipeline remains strictly linear until post-Stylize expansion approval

---

## Testing Strategy (Future)

### Unit Tests

**Orchestrator**:
- Test aggregation logic with mocked tool outputs
- Test error handling (timeout, crash, invalid JSON)
- Test status determination rules

**Individual Tools**:
- Test each verification check independently
- Test edge cases (missing files, invalid data)
- Test JSON output formatting

### Integration Tests

- Run full pipeline end-to-end
- Verify output schema compliance
- Test on various system states (healthy, degraded, broken)

---

## Summary

The verification execution flow is:

1. **Linear**: Fixed sequential tool execution
2. **Stateless**: No session or context persistence
3. **Deterministic**: Reproducible results
4. **Isolated**: Tools execute independently
5. **Offline**: No external dependencies
6. **Standardized**: Unified JSON output format
7. **Minimal**: No complex logic in navigation layer

This flow serves as the baseline implementation for system verification, designed to be simple, predictable, and maintainable while preserving strict A.N.T. layer separation.

---

**Last Updated**: 2026-02-13T21:35:00+05:00  
**Status**: Baseline flow documented — orchestrator implemented, CLI integration pending
