# Offline Data Management SOP

> **Purpose**: Define how Omni-Nexus manages data flow without external API dependencies  
> **Derived From**: North Star (offline AI workflows) + Source of Truth (local JSON/markdown)  
> **Status**: Blueprint Phase

---

## Core Principle

All data operations must function in **fully offline environments**. The system never assumes network connectivity.

---

## Data Storage Strategy

### 1. Local File System as Single Source of Truth

**Primary Data Locations**:
- `agents/_registry.json` — Agent metadata
- `.tmp/logs/*.log` — Structured event logs
- `.tmp/cache/` — Temporary computation results
- `.tmp/sessions/` — Active workflow states
- `architecture/` — System blueprints (read-only after Blueprint)

**Invariant**: No data stored in external databases, cloud storage, or APIs.

---

### 2. Data Flow Patterns

```
User Input (CLI)
  ↓
Navigation Layer (routing decision)
  ↓
Agent/Tool Execution (read local data)
  ↓
Tools Layer (write local data)
  ↓
Output Formatter (CLI stdout or file export)
```

**Rule**: Data never leaves the local file system boundary.

---

## File Operations Protocol

### Atomic Writes

All file mutations must use atomic write pattern:

1. Write to temporary file (`.tmp` suffix)
2. Validate file integrity (JSON parse, schema check)
3. Atomic move to final location
4. Log operation success

**Never** write directly to production files — prevents corruption.

---

### Read Operations

**Before Reading**:
1. Verify file exists
2. Check file is not empty
3. Attempt parse (JSON/text)
4. Handle errors gracefully (return `None` or default)

**Never** crash on missing files — log warning and continue.

---

## Data Schemas

All JSON payloads must conform to schemas defined in `gemini.md`.

**Validation Points**:
- Before writing to registry
- Before spawning agents
- Before routing tasks
- Before tool execution

**Schema Violations** → error recovery, not crashes.

---

## Offline Constraints

### No External Dependencies

- ❌ No API calls
- ❌ No database connections
- ❌ No network requests
- ✅ Pure file system operations
- ✅ In-memory computation
- ✅ Local process execution

### Data Persistence

**Session Data** (`.tmp/sessions/`):
- Active workflow states
- Cleared on system restart
- Not guaranteed persistent

**Permanent Data** (`agents/`, root files):
- Survives restarts
- Must be backed up manually by user
- Version controlled (Git recommended)

---

## Cache Management

### Temporary Files (`.tmp/`)

**Lifecycle**:
- Created during execution
- Auto-deleted after workflow completes
- Never relied on for critical state

**Cache Invalidation**:
- Time-based (older than session)
- Size-based (if exceeds threshold)
- Manual (`cli/main.py clear-cache`)

---

## Data Export

**Supported Export Formats**:
- JSON (structured data)
- Markdown (reports, logs)
- Plain text (stdout)

**Export Destinations**:
- CLI stdout (primary)
- Local files (`.tmp/exports/`)
- User-specified paths

**Never** export to network locations automatically.

---

## Backup Strategy

**User Responsibility**:
- Omni-Nexus does NOT auto-backup
- Users must manually backup:
  - `agents/` directory
  - Root memory files (`task_plan.md`, etc.)
  - `architecture/` documentation

**Recommended**: Git version control for entire workspace.

---

## Edge Cases

### File Corruption

If JSON file is corrupted:
1. Log error to `.tmp/logs/system.log`
2. Attempt load from `.bak` backup (if exists)
3. If no backup, initialize empty structure
4. Alert user via CLI warning

### Disk Full

If write fails due to disk space:
1. Log critical error
2. Halt execution gracefully
3. Display error message to user
4. Do NOT attempt retry (may worsen)

### Concurrent Access

**Not Supported**: Multiple Omni-Nexus instances on same workspace.

If detected (lock file exists):
- Exit with error message
- Instruct user to close other instances

---

## Compliance Checklist

Every data operation must:
- [ ] Use atomic write pattern
- [ ] Validate schema before commit
- [ ] Log operation to appropriate service log
- [ ] Handle errors without crashing
- [ ] Never assume network availability
- [ ] Never mutate architecture files post-Blueprint

---

## Summary

Offline-first data management ensures:
- **Reliability**: No network failures
- **Privacy**: Data never leaves local machine
- **Determinism**: Same inputs always produce same outputs
- **Safety**: Atomic operations prevent corruption
