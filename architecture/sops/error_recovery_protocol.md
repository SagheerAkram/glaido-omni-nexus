# Error Recovery Protocol SOP

> **Purpose**: Define self-annealing repair loop mechanics for automatic error recovery  
> **Derived From**: System Invariants (self-repair) + North Star (autonomous operation)  
> **Status**: Blueprint Phase

---

## Core Principle

When any tool or agent fails, the system must **automatically diagnose, patch, and recover** without manual intervention. This is the self-annealing repair loop.

---

## Error Detection

### 1. Tool Execution Failures

**Detection Points**:
- Tool script exits with non-zero code
- Tool raises unhandled exception
- Tool timeout (exceeds expected duration)
- Tool produces invalid output (schema validation fails)

**Logged To**: `.tmp/logs/<service>.log`

---

### 2. Agent Execution Failures

**Detection Points**:
- Agent behavior script crashes
- Agent returns error status in payload
- Agent fails to respond within timeout
- Agent produces malformed output

**Logged To**: `.tmp/logs/agents.log`

---

### 3. Navigation Routing Failures

**Detection Points**:
- No valid route found for task type
- Routing decision validation fails
- Target agent/tool does not exist

**Logged To**: `.tmp/logs/navigation.log`

---

## Recovery Loop Workflow

### Phase 1: Error Capture

```
1. Tool/Agent executes
2. Exception raised or non-zero exit
3. Error handler catches exception
4. Log full error details:
   - Error type
   - Stack trace
   - Input payload
   - Expected output
   - Timestamp
5. Return error routing decision
```

---

### Phase 2: Diagnosis

```
1. Navigation receives error routing decision
2. Analyze error log entry
3. Determine error category:
   - Missing dependency
   - Invalid input
   - File corruption
   - Logic error
   - Timeout
4. Select recovery strategy
```

**Error Categories**:

| Error Type | Recovery Strategy |
|------------|-------------------|
| Missing file | Create with defaults |
| Invalid schema | Validate and sanitize |
| Tool crash | Retry with fallback |
| Agent timeout | Kill and respawn |
| Routing failure | Use default handler |

---

### Phase 3: Automatic Patch

**For Tool Errors**:
1. Read tool source code
2. Identify problematic line (from stack trace)
3. Generate patch (if simple fix):
   - Missing import → Add import
   - Wrong path → Correct path
   - Type error → Add type conversion
4. Apply patch to tool script
5. Retest tool

**For Agent Errors**:
1. Check agent config validity
2. If config invalid → Reset to template
3. If behavior.py corrupted → Regenerate from stub
4. Update registry entry status to "recovering"

**For Data Errors**:
1. If JSON corrupted → Load from `.bak` backup
2. If no backup → Initialize empty structure
3. Log data loss warning

---

### Phase 4: Retry Execution

```
1. Re-execute failed operation with patched code
2. Monitor for success/failure
3. If success:
   - Log recovery success
   - Update SOP documentation (prevent future occurrence)
   - Return result to user
4. If failure persists:
   - Escalate to fallback handler
```

---

### Phase 5: SOP Update (Learning)

**Invariant**: Every error must update architecture to prevent recurrence.

**Update Process**:
1. Identify which SOP/specification governs the failed operation
2. Add edge case to appropriate `architecture/edge_cases/*.md`
3. Update tool specification with new constraint
4. Log architectural change

**Example**:
- Tool crashes on empty file
- Edge case added to `data_corruption_recovery.md`
- Tool updated to check file size before read
- SOP documents: "All file reads must verify non-empty"

---

## Fallback Strategies

### Tool Fallback Chain

```
Primary Tool → Backup Tool → Manual Intervention Required
```

**Example**:
- `tools/data/file_ops.py` fails
- Fallback to Python stdlib `open()` directly
- If stdlib fails, return error to user

---

### Agent Fallback Chain

```
Specialized Agent → Generic Agent → Direct Tool Call
```

**Example**:
- `agent_discovery` fails
- Fallback to generic `agent_execution`
- If still fails, call tool directly without agent

---

### Routing Fallback

```
Specific Route → Default Handler → Error Response
```

**Example**:
- Task type "unknown_type" has no route
- Router uses default generic handler
- Handler returns structured error payload

---

## Timeout Handling

### Tool Timeouts

**Default Timeout**: 30 seconds per tool

**On Timeout**:
1. Kill tool process
2. Log timeout error
3. Check for partial output
4. If partial output usable → return with warning
5. If no output → retry once with 2x timeout
6. If retry fails → escalate to fallback

---

### Agent Timeouts

**Default Timeout**: 60 seconds per agent task

**On Timeout**:
1. Mark agent as "unresponsive"
2. Spawn replacement agent (same type)
3. Re-send task to new agent
4. Original agent auto-terminated after grace period

---

## Error Logging Format

### Structured Error Log

```json
{
  "timestamp": "2026-02-13T21:18:00+05:00",
  "service": "tools",
  "error_type": "FileNotFoundError",
  "component": "tools/data/file_ops.py",
  "function": "read_json",
  "input_payload": {"file_path": "/missing/file.json"},
  "stack_trace": "...",
  "recovery_attempted": true,
  "recovery_strategy": "create_default_file",
  "recovery_success": true,
  "duration_ms": 234
}
```

---

## Recovery Metrics

Track recovery effectiveness:

```json
{
  "total_errors": 100,
  "auto_recovered": 92,
  "manual_intervention": 8,
  "recovery_rate": 0.92
}
```

**Goal**: 90%+ auto-recovery rate

---

## Edge Cases

### Cascading Failures

If recovery attempt causes new error:
1. Detect circular error pattern
2. Halt recovery loop (prevent infinite recursion)
3. Log critical error
4. Return to user with full error chain

---

### Corrupted Architecture Files

If `architecture/*.md` files corrupted:
1. **DO NOT** attempt auto-repair
2. Architecture is read-only post-Blueprint
3. Alert user immediately
4. Halt system until manual fix

---

## Behavioral Rules

### Never Silently Fail

- All errors logged
- User notified of recovery attempts
- Warnings shown for fallback usage

### Deterministic Recovery

- Same error + same state = same recovery strategy
- No randomness in patch selection
- Recovery path documented

### Preserve User Data

- Never delete user files during recovery
- Always create backups before mutation
- Data loss logged as critical error

---

## Summary

Self-annealing repair ensures:
- **Autonomous Operation**: Most errors self-resolve
- **System Learning**: Architecture improves from failures
- **User Trust**: Transparent error handling
- **Reliability**: Graceful degradation, not crashes
