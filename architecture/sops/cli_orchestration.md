# CLI Orchestration SOP

> **Purpose**: Define how CLI commands trigger multi-agent workflows  
> **Derived From**: Delivery Payload (CLI stdout) + North Star (orchestration ecosystem)  
> **Status**: Blueprint Phase

---

## Core Principle

The CLI is the **primary interface** for triggering orchestrated workflows. All user interaction flows through command-line arguments.

---

## Command Structure

### Base Pattern

```
python cli/main.py <command> [subcommand] [--options]
```

**Examples**:
- `python cli/main.py init`
- `python cli/main.py agent spawn --config <json>`
- `python cli/main.py workflow run --id <workflow_id>`

---

## Command Categories

### 1. System Commands

**Purpose**: Initialize, diagnose, configure

- `init` — Initialize system, run diagnostics
- `status` — Show current system state
- `diagnostic` — Run full health check
- `config` — View/update configuration
- **`verify`** — **First Operational Trigger Endpoint** (Phase 5)

**Orchestration**: 
- Most commands: None (direct tool calls)
- **`verify` orchestration** (activated in Phase 5):
  * Derived from: `architecture/specifications/verification_display_contract.md` (Stylize phase)
  * Flow: `CLI verify → cli/display/verification_renderer → navigation/orchestrator/verification_orchestrator → tools`
  * Boundary: Presentation layer (renderer) invokes Navigation layer (orchestrator) which executes Tools layer
  * Key Principle: Trigger activates existing capabilities defined in Stylize, introduces no new execution logic

---

### 2. Agent Commands

**Purpose**: Manage agent lifecycle

- `agent list` — List registered agents
- `agent spawn --config <json>` — Create new agent
- `agent info --id <agent_id>` — Get agent details
- `agent remove --id <agent_id>` — Deregister agent

**Orchestration**: 
- Command → CLI parser
- CLI → Navigation/task_router
- Router → tools/agents/agent_spawner.py
- Spawner → Write agent files + update registry
- Return success/failure to CLI

---

### 3. Workflow Commands

**Purpose**: Execute multi-step processes

- `workflow list` — List available workflows
- `workflow run --id <workflow_id>` — Execute workflow
- `workflow status --id <workflow_id>` — Check workflow progress

**Orchestration**:
- Command → CLI parser
- CLI → Navigation/workflow_manager
- Manager → Spawn required agents
- Agents → Execute tasks via tools
- Manager → Aggregate results
- Return output to CLI stdout

---

### 4. Task Commands

**Purpose**: Route one-off tasks

- `task route --json <payload>` — Route task to agent/tool
- `task execute --type <type> --payload <json>` — Direct execution

**Orchestration**:
- Command → CLI parser
- CLI → Navigation/task_router
- Router → Determine target (agent or tool)
- Execute → Log to service log
- Return result to CLI stdout

---

## Orchestration Flow

### Single-Agent Task

```
User: python cli/main.py task execute --type diagnostic

1. CLI parses arguments
2. CLI calls navigation/task_router.route({
     task_id: "task_001",
     task_type: "diagnostic",
     payload: {}
   })
3. Router determines: "diagnostic" → tools/core/diagnostics.py
4. Router creates routing_decision
5. CLI executes: python tools/core/diagnostics.py
6. Tool returns JSON result
7. CLI formats output with ANSI colors
8. CLI prints to stdout
```

---

### Multi-Agent Workflow

```
User: python cli/main.py workflow run --id agent_coordination_test

1. CLI parses arguments
2. CLI calls navigation/workflow_manager.execute("agent_coordination_test")
3. Workflow Manager reads workflow definition
4. Manager spawns agents: [discovery_agent, execution_agent, monitoring_agent]
5. Manager coordinates:
   - discovery_agent → finds data sources
   - execution_agent → processes data
   - monitoring_agent → validates results
6. Manager aggregates outputs
7. Manager logs workflow completion
8. CLI receives final payload
9. CLI formats and prints to stdout
```

---

## Output Formatting

### Success Output

```
[✓] Operation completed successfully
Result: <formatted_output>
```

**ANSI Colors**:
- Success icon: Lime Green
- Text: White

---

### Error Output

```
[✗] Operation failed
Error: <error_message>
```

**ANSI Colors**:
- Error icon: White
- Text: White

---

### Progress Output

For long-running tasks:

```
[●] Processing step 1/5...
[●] Processing step 2/5...
...
```

**ANSI Colors**:
- Progress icon: Lime Green
- Text: White

---

## Argument Parsing

### Required vs Optional

**Required** (fails if missing):
- `--config` for `agent spawn`
- `--id` for specific operations

**Optional** (has defaults):
- `--json` for output format
- `--verbose` for detailed logs

---

### JSON Argument Handling

**Inline JSON**:
```
--config '{"agent_id": "agent_test", "name": "Test"}'
```

**File-based JSON**:
```
--config @config/agent_config.json
```

**Validation**:
1. Parse JSON
2. Validate against schema (via tools/core/validator.py)
3. If invalid, return error immediately (don't execute)

---

## Error Handling

### User Input Errors

**Invalid command**:
```
[✗] Unknown command: 'invalid'
Run 'python cli/main.py --help' for usage
```

**Missing argument**:
```
[✗] Missing required argument: --config
Run 'python cli/main.py agent spawn --help'
```

---

### Execution Errors

**Tool failure**:
```
[✗] Tool execution failed: tools/core/diagnostics.py
Error: File not found
Check logs: .tmp/logs/system.log
```

**Agent failure**:
```
[✗] Agent 'agent_test' failed to execute
Error: Invalid payload schema
Check logs: .tmp/logs/agents.log
```

---

## Logging Integration

Every CLI command must:
1. Log command invocation to `.tmp/logs/cli.log`
2. Log routing decision (if applicable)
3. Log final result (success/failure)

**Log Format**:
```json
{
  "timestamp": "2026-02-13T21:15:00+05:00",
  "command": "agent spawn",
  "arguments": {"config": "..."},
  "result": "success",
  "duration_ms": 1234
}
```

---

## Behavioral Rules

### Professional Output

- ❌ No informal language
- ❌ No unnecessary verbosity
- ✅ Concise, structured messages
- ✅ Clear success/failure indicators

### Deterministic Behavior

- Same command + same state = same output
- No randomness in routing decisions
- No timestamp-dependent logic (except logging)

### Never Crash

- Invalid input → error message, not crash
- Tool failure → log error, return gracefully
- Unknown command → help message, not crash

---

## Future Extensions

### Interactive Mode (Phase 5)

**Not in Blueprint**:
- Long-running REPL
- Auto-complete
- Command history

**Current**: One-shot command execution only

---

## Summary

CLI orchestration ensures:
- **User Control**: All workflows triggered explicitly
- **Transparency**: Clear output formatting
- **Reliability**: Error handling at every step
- **Offline-First**: No network dependencies in command flow
