# Agent Failure Modes

> **Purpose**: Document agent crash scenarios and recovery strategies  
> **Derived From**: Error Recovery Protocol + Agent Specifications  
> **Status**: Blueprint Phase — Edge Cases

---

## Failure Categories

### 1. Spawn Failures

**Scenario**: Agent creation fails during spawn process

**Causes**:
- Invalid agent config (schema validation fails)
- Duplicate agent_id in registry
- Disk full (cannot create agent directory)
- File system permissions error

**Symptoms**:
- `agent_spawner.py` returns False
- Error logged to `.tmp/logs/agents.log`
- Agent not added to registry

**Recovery Strategy**:
1. Validate config before spawn attempt
2. Check agent_id uniqueness
3. Verify disk space available
4. If spawn fails, return structured error to user
5. Do NOT create partial agent (clean up on failure)

**Prevention**:
- Schema validation before spawn
- Disk space check before file creation
- Registry locking during spawn

---

### 2. Execution Timeout

**Scenario**: Agent does not complete task within timeout

**Causes**:
- Infinite loop in agent logic
- Blocking I/O operation
- Heavy computation exceeding limit
- Deadlock with tool execution

**Symptoms**:
- Agent process still running after timeout
- No output returned
- CPU usage stuck at 100%

**Recovery Strategy**:
1. Navigation detects timeout (60s default)
2. Send SIGTERM to agent process
3. Wait 5 seconds for graceful shutdown
4. If still running, send SIGKILL
5. Mark agent as "unresponsive" in registry
6. Spawn replacement agent (same type)
7. Re-send task to new agent
8. Log timeout event

**Prevention**:
- Design agents with short execution times
- Delegate heavy work to tools
- Use async patterns for I/O

---

### 3. Logic Errors

**Scenario**: Agent behavior.py has bug causing crash

**Causes**:
- Unhandled exception in execute()
- Type error (wrong input type)
- Division by zero
- Index out of bounds
- Missing import

**Symptoms**:
- Python stack trace in logs
- Agent returns error status
- Exit code non-zero

**Recovery Strategy**:
1. Catch exception in agent wrapper
2. Log full stack trace
3. Return structured error payload:
   ```json
   {
     "task_id": "...",
     "status": "error",
     "error": "Exception message",
     "stack_trace": "..."
   }
   ```
4. Navigation receives error
5. Error recovery protocol activated
6. If simple fix (e.g., missing import):
   - Auto-patch behavior.py
   - Retry execution
7. If complex error:
   - Return error to user
   - Log to architecture edge cases

**Prevention**:
- Try-catch blocks in execute()
- Input validation before processing
- Type hints in behavior.py
- Unit tests for agent logic

---

### 4. Invalid Output

**Scenario**: Agent returns malformed output payload

**Causes**:
- Missing required fields (task_id, status)
- Wrong schema format
- JSON serialization error
- Empty output

**Symptoms**:
- Schema validation fails on output
- Navigation cannot parse result
- Routing decision cannot be created

**Recovery Strategy**:
1. Navigation validates agent output
2. If invalid, log validation error
3. Treat as execution error
4. Return error to caller:
   ```json
   {
     "task_id": "...",
     "status": "error",
     "error": "Agent returned invalid output schema"
   }
   ```
5. Update agent specification to clarify schema
6. Mark agent for review

**Prevention**:
- Output schema validation in agent code
- Use template response objects
- Test agent outputs during development

---

### 5. Dependency Failures

**Scenario**: Agent requires tool that doesn't exist

**Causes**:
- Agent config lists non-existent tool
- Tool file deleted after agent spawn
- Tool path misconfigured

**Symptoms**:
- Agent tries to call tool, gets FileNotFoundError
- Agent execution fails immediately
- Logs show "tool not found"

**Recovery Strategy**:
1. Agent startup validates all dependencies exist
2. If tool missing:
   - Log error
   - Return dependency error to caller
   - Do NOT attempt execution
3. Navigation receives error
4. If tool should exist:
   - Error recovery creates missing tool from template
   - Retry agent execution
5. If tool intentionally removed:
   - User notified
   - Agent marked as "dependency_error"

**Prevention**:
- Validate dependencies during spawn
- Check tool existence before agent registration
- Document tool requirements in manifest.md

---

### 6. State Corruption

**Scenario**: Agent's config.json becomes corrupted

**Causes**:
- Disk failure during write
- Power loss mid-update
- Manual file editing error
- JSON parse error

**Symptoms**:
- Cannot load agent config
- JSON parsing fails
- Missing required fields

**Recovery Strategy**:
1. Attempt to load `config.json`
2. If fails, check for `config.json.bak` backup
3. If backup exists and valid:
   - Restore from backup
   - Log restoration event
   - Continue execution
4. If no backup or backup corrupt:
   - Regenerate config from registry entry
   - Log data loss warning
   - Mark agent as "recovered"
5. If registry also corrupt:
   - Agent cannot be recovered
   - User notification required

**Prevention**:
- Atomic writes with .bak backups
- Registry as backup source of truth
- Never edit config.json directly

---

### 7. Zombie Agents

**Scenario**: Agent process remains running after task completion

**Causes**:
- Agent fails to exit after return
- Infinite background thread
- Unclosed file handles
- Signal handling error

**Symptoms**:
- Process still in OS process list
- No CPU usage but not terminating
- Lock file not released

**Recovery Strategy**:
1. Navigation tracks agent process IDs
2. After timeout (grace period 30s after task return):
   - Check if process still exists
   - Send SIGTERM
   - Wait 5 seconds
   - If still exists, send SIGKILL
3. Log zombie cleanup event
4. Clean up lock files
5. Register cleanup in error recovery log

**Prevention**:
- Ensure agents exit cleanly
- No background threads
- Properly close resources
- Use context managers

---

### 8. Cascading Failures

**Scenario**: One agent failure triggers other agent failures

**Causes**:
- Agent A output required by Agent B
- Agent A fails, Agent B gets invalid input
- Workflow coordination breaks down

**Symptoms**:
- Multiple agent errors in sequence
- Workflow unable to complete
- Error logs show dependency chain

**Recovery Strategy**:
1. Workflow manager detects first failure
2. Halt remaining workflow steps
3. Log cascading failure pattern
4. Return error to user with full chain:
   ```json
   {
     "workflow_id": "...",
     "status": "error",
     "failed_at": "step_2",
     "error_chain": [
       {"step": "step_1", "agent": "agent_A", "error": "..."},
       {"step": "step_2", "agent": "agent_B", "error": "Input validation failed"}
     ]
   }
   ```
5. Do NOT attempt auto-recovery (too complex)
6. User notification required

**Prevention**:
- Validate inputs between workflow steps
- Fallback agents for critical steps
- Circuit breaker pattern in workflows

---

## Recovery Decision Matrix

| Failure Type | Auto-Recover? | Strategy |
|--------------|---------------|----------|
| Spawn failure | No | Return error to user |
| Timeout | Yes | Kill and respawn |
| Logic error | Maybe | Patch if simple, else error |
| Invalid output | No | Return schema error |
| Dependency | Yes | Create missing tool |
| Corruption | Yes | Restore from backup |
| Zombie | Yes | Force kill |
| Cascading | No | Halt and notify user |

---

## Monitoring & Detection

### Agent Health Check

Periodic check (via monitoring agents):
1. Verify all registered agents have valid folders
2. Check config.json integrity
3. Validate no zombie processes
4. Monitor execution success rate

**Frequency**: On-demand (not automatic in v1.0)

---

## Summary

Agent failure modes covered:
- **Spawn failures** — Creation errors
- **Timeouts** — Unresponsive agents
- **Logic errors** — Code bugs
- **Invalid outputs** — Schema violations
- **Dependencies** — Missing tools
- **Corruption** — File integrity
- **Zombies** — Process cleanup
- **Cascading** — Workflow failures

All failures logged, most auto-recoverable, complex ones escalate to user.
