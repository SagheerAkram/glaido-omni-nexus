# Execution Constraints

> **Purpose**: Define offline-first behavioral rules and system boundaries  
> **Derived From**: Behavioral Rules (offline-only) + Source of Truth (local files)  
> **Status**: Blueprint Phase

---

## Primary Constraint: Offline-Only Operation

**Absolute Rule**: Omni-Nexus MUST function with **zero network connectivity**.

All components designed assuming:
- No internet access
- No external APIs
- No cloud services
- No database connections
- No network file systems

---

## File System Boundaries

### Workspace Root

All operations confined to workspace root directory:

```
<workspace_root>/
├── agents/
├── architecture/
├── cli/
├── navigation/
├── tools/
├── .tmp/
└── [root memory files]
```

**Prohibited**:
- ❌ Writing outside workspace
- ❌ Reading system files (e.g., `/etc/`)
- ❌ Accessing user home directory (except workspace)
- ❌ Network mounts or UNC paths

**Allowed**:
- ✅ Read/write within workspace
- ✅ Temporary files in `.tmp/`
- ✅ Log files in `.tmp/logs/`

---

## Execution Time Constraints

### Tool Execution Limits

| Tool Type | Max Duration |
|-----------|--------------|
| File I/O | 10 seconds |
| Data transformation | 30 seconds |
| Diagnostics | 30 seconds |
| Agent spawn | 15 seconds |

**On Timeout**:
- Kill process
- Log timeout error
- Return error payload
- Do NOT retry automatically (escalate to error recovery)

---

### Agent Execution Limits

| Agent Type | Max Duration |
|-----------|--------------|
| Discovery | 60 seconds |
| Execution | 120 seconds |
| Monitoring | 30 seconds |
| Custom | 60 seconds |

**On Timeout**:
- Mark agent as unresponsive
- Spawn replacement agent
- Log timeout event

---

## Resource Constraints

### Memory Limits

**Per Process**:
- CLI: 100 MB
- Tool: 50 MB
- Agent: 100 MB
- Navigation: 50 MB

**Enforcement**:
- Not hard-enforced (OS dependent)
- Design targets only
- Avoid loading large files entirely into memory

---

### Disk Usage Limits

**Temporary Files** (`.tmp/`):
- Max total size: 1 GB
- Auto-cleanup when exceeds threshold
- FIFO deletion (oldest first)

**Log Files** (`.tmp/logs/`):
- Max per log: 10 MB
- Rotation when exceeds limit
- Keep last 3 rotations

**Agent Files** (`agents/`):
- No hard limit
- Each agent ~10 KB (config + manifest + behavior)
- Expected max: 1000 agents = 10 MB

---

## Concurrency Constraints

### Single Instance Only

**Prohibited**:
- Multiple Omni-Nexus processes on same workspace
- Concurrent CLI commands on same workspace

**Enforcement**:
- Lock file: `.tmp/.omni-nexus.lock`
- Created on CLI start
- Deleted on CLI exit
- Check exists before any operation

---

### Sequential Task Execution

**Current Design**:
- One task at a time
- No parallel task execution within single CLI invocation
- Workflows execute steps sequentially

**Future** (Phase 5):
- Parallel workflow steps
- Concurrent agent execution
- Not in Blueprint scope

---

## Data Integrity Constraints

### Atomic Operations

**All writes must be atomic**:
1. Write to temp file
2. Validate content
3. Atomic move to final location

**Never**:
- Partial writes
- Direct overwrites
- Concurrent modifications

---

### Backup Before Mutation

**Required for**:
- Agent registry updates
- Configuration changes
- Schema modifications

**Pattern**:
- Create `.bak` file before write
- Keep last backup only
- Restore from backup on corruption

---

## Dependency Constraints

### Python Standard Library Only

**Allowed**:
- Built-in Python modules
- Standard library (json, pathlib, sys, etc.)

**Prohibited**:
- External libraries (unless explicitly vendored)
- Network-dependent packages
- Binary dependencies requiring compilation

**Exception**:
- Core Python runtime assumed installed

---

### No External Binaries

**Prohibited**:
- Calling external executables (git, curl, etc.)
- Shell script execution
- System command invocation

**Allowed**:
- Python subprocess for Python scripts only
- JSON parsing
- File system operations

---

## Architecture Immutability

### Post-Blueprint Freeze

Once Blueprint phase complete:

**Read-Only**:
- `architecture/` directory
- All SOP documents
- All specification files

**Prohibited**:
- Modifying architecture files during runtime
- Auto-generated architecture patches
- Dynamic SOP updates

**Exception**:
- Edge case documentation updates (manual only)
- Version-controlled changes

---

## Privacy & Security Constraints

### No External Data Leakage

**Prohibited**:
- Sending data to external services
- Logging to cloud services
- Telemetry or analytics
- Crash reporting to external servers

**Allowed**:
- Local file logging only
- User-initiated export
- Manual data sharing (user copies files)

---

### No Authentication

**System Design**:
- No user accounts
- No password management
- No API keys for external services

**Rationale**:
- Offline-only system
- Single-user workspace
- OS-level access control sufficient

---

## Error Handling Constraints

### Never Crash

**Required Behavior**:
- Invalid input → error message, not exception
- Missing file → warning, continue with defaults
- Tool failure → log error, retry or fallback

**Prohibited**:
- Unhandled exceptions reaching user
- Abrupt process termination
- Silent failures

---

### Graceful Degradation

**Fallback Hierarchy**:
1. Primary tool/agent
2. Fallback tool/agent
3. Default error handler
4. User notification

**Never**:
- Leave system in broken state
- Corrupt data on failure
- Lose user input

---

## Determinism Constraints

### Reproducible Execution

**Given**:
- Same input payload
- Same workspace state
- Same agent configuration

**Result**:
- Same output
- Same routing decisions
- Same tool execution

**Prohibited**:
- Random number generation (unless seeded)
- Timestamp-based logic (except logging)
- Non-deterministic algorithms

---

## Testing Constraints

### All Tools Testable

**Required**:
- Every tool has CLI test mode
- Accepts JSON input via argv
- Returns structured JSON output

**Pattern**:
```
python tools/core/validator.py '{"test": "data"}'
```

---

### No Mock Data in Production

**Test Data Location**: `tests/fixtures/`

**Prohibited**:
- Hardcoded test data in production tools
- Mock responses in agent logic
- Fake file system operations

---

## Summary

Execution constraints ensure:
- **Offline Independence**: Zero network requirements
- **Resource Efficiency**: Bounded memory/disk usage
- **Data Safety**: Atomic operations, backups
- **Determinism**: Reproducible execution
- **Reliability**: Graceful degradation, no crashes
- **Privacy**: No external data leakage
