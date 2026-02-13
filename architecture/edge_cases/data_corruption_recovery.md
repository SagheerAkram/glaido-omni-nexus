# Data Corruption Recovery

> **Purpose**: File integrity strategies and corruption recovery protocols  
> **Derived From**: Offline Data Management + Error Recovery Protocol  
> **Status**: Blueprint Phase — Edge Cases

---

## Corruption Scenarios

### 1. JSON File Corruption

**Affected Files**:
- `agents/_registry.json`
- Agent `config.json` files
- Workflow definitions
- Any structured data files

**Symptoms**:
- JSON parsing fails
- Missing closing braces
- Invalid UTF-8 characters
- Truncated file content

**Detection**:
```python
try:
    data = json.loads(file.read_text())
except json.JSONDecodeError as e:
    # Corruption detected
    log_error(f"JSON corruption: {e}")
```

---

#### Recovery Strategy: JSON Corruption

**Step 1: Attempt Backup Restore**
```
1. Check for .bak file (e.g., _registry.json.bak)
2. If exists:
   - Validate backup is valid JSON
   - If valid: restore from backup
   - Log restoration event
   - Return restored data
```

**Step 2: Attempt Partial Parse**
```
3. If backup missing or also corrupt:
   - Read file as text
   - Try to extract salvageable JSON fragments
   - Use regex to find complete objects
   - Reconstruct partial data structure
```

**Step 3: Initialize Empty**
```
4. If no recovery possible:
   - Initialize empty structure:
     {
       "agents": [],
       "last_updated": "<now>",
       "schema_version": "1.0"
     }
   - Log data loss warning
   - Create new backup
```

**Step 4: User Notification**
```
5. Always notify user of corruption:
   [!] Warning: _registry.json was corrupted
   [●] Restored from backup (age: 2 hours)
   [●] Data loss: 0 entries
```

---

### 2. Log File Corruption

**Affected Files**:
- `.tmp/logs/system.log`
- `.tmp/logs/agents.log`
- `.tmp/logs/navigation.log`
- All service logs

**Symptoms**:
- Incomplete log entries
- Binary garbage in text file
- Missing newlines
- Invalid JSON in structured logs

---

#### Recovery Strategy: Log Corruption

**Step 1: Isolate Corruption**
```
1. Read log file line by line
2. Identify invalid lines (JSON parse fails)
3. Skip corrupted lines
4. Continue with valid lines
```

**Step 2: Archive Corrupted Log**
```
5. Move corrupted log to .tmp/logs/corrupted/
6. Create fresh log file
7. Log corruption event to new file
```

**Step 3: No Data Recovery Needed**
```
8. Logs are append-only, non-critical
9. Loss of log history acceptable
10. System continues normally
```

**User Notification**: Optional (only if --verbose)

---

### 3. Markdown File Corruption

**Affected Files**:
- Agent `manifest.md`
- Architecture SOPs
- Root memory files (`task_plan.md`, etc.)

**Symptoms**:
- Garbled text
- Binary content in text file
- Encoding errors

---

#### Recovery Strategy: Markdown Corruption

**Step 1: Architecture Files**
```
1. Architecture files are READ-ONLY post-Blueprint
2. If corrupted:
   - CRITICAL ERROR
   - Halt system
   - User must restore from version control
   - No automatic recovery
```

**Step 2: Agent Manifest**
```
3. Agent manifests can be regenerated
4. If corrupted:
   - Regenerate from agent config.json
   - Use manifest template
   - Populate with config data
   - Log regeneration event
```

**Step 3: Root Memory Files**
```
5. task_plan.md, findings.md, etc.
6. If corrupted:
   - Check for .bak backup
   - If exists: restore
   - If not: user must restore manually
   - Log critical warning
```

---

### 4. Agent Directory Corruption

**Scenario**: Entire agent folder damaged or deleted

**Symptoms**:
- Agent folder missing
- Some agent files missing
- File permissions broken

---

#### Recovery Strategy: Agent Directory

**Step 1: Detect Missing Agent**
```
1. Registry shows agent exists
2. Agent folder not found at path
3. Log critical error
```

**Step 2: Attempt Respawn**
```
4. If agent spawnable (has registry entry):
   - Extract config from registry
   - Respawn agent from scratch
   - Regenerate all files
   - Mark as "regenerated" in registry
```

**Step 3: Partial Recovery**
```
5. If only some files missing:
   - Regenerate missing files from templates
   - Preserve existing valid files
   - Log partial recovery
```

**Step 4: Registry Cleanup**
```
6. If agent cannot be recovered:
   - Remove from registry
   - Log permanent loss
   - User notification
```

---

### 5. Backup File Corruption

**Scenario**: Both primary and backup files corrupted

**Symptoms**:
- `.bak` file also invalid
- Multiple corruption events in short time
- Disk errors in system logs

---

#### Recovery Strategy: Double Corruption

**Step 1: Escalate to Critical**
```
1. Log CRITICAL error
2. Both primary and backup corrupt = disk issue
3. Halt current operation
```

**Step 2: Diagnostic Check**
```
4. Run file system integrity check:
   - Verify workspace directory readable
   - Check disk space
   - Test write permissions
```

**Step 3: Initialize Empty**
```
5. If disk OK:
   - Initialize empty structure
   - DO NOT create backup (disk may be failing)
   - Log data loss
```

**Step 4: User Alert**
```
6. Critical alert to user:
   [✗] CRITICAL: Multiple file corruption detected
   [!] Possible disk failure
   [!] Data loss: <affected_files>
   [●] Recommendation: Backup entire workspace immediately
```

---

## Corruption Prevention

### Atomic Write Pattern

**Always Use**:
```python
def atomic_write(path, data):
    temp_path = path.with_suffix('.tmp')
    
    # Write to temp
    temp_path.write_text(json.dumps(data, indent=2))
    
    # Validate temp file
    validate_json(temp_path)
    
    # Create backup before overwrite
    if path.exists():
        backup_path = path.with_suffix('.bak')
        shutil.copy2(path, backup_path)
    
    # Atomic move
    shutil.move(str(temp_path), str(path))
```

**Never**:
- Direct overwrites
- Partial writes
- Concurrent writes

---

### Backup Rotation

**Strategy**:
- Keep last known good backup
- Overwrite backup only after successful validation
- Never delete backup before new data validated

**Not Implemented**:
- Multiple backup versions (only last .bak)
- Timestamped backups
- Off-site backups (offline constraint)

---

### File Locking

**Current Design**:
- No file-level locking (overhead)
- Process-level lock (`.tmp/.omni-nexus.lock`)
- Single-instance enforcement prevents concurrent writes

**Future**:
- Advisory file locks (fcntl on Unix)
- Not in Blueprint scope

---

## Corruption Detection

### Proactive Checks

**On Read**:
1. Verify file exists
2. Check file size > 0
3. Attempt parse (JSON/text)
4. Validate schema if applicable

**On Write**:
1. Validate data before write
2. Verify temp file after write
3. Check final file after atomic move

---

### Reactive Checks

**Diagnostic Tool**:
- `python tools/core/diagnostics.py`
- Checks all critical files
- Reports corruption if found

**Manual Check**:
- User can validate entire workspace
- Future: `python cli/main.py validate-workspace`

---

## Recovery Success Metrics

**Trackable Metrics**:
- Corruption events detected
- Successful backup restores
- Data loss events (unrecoverable)
- Regeneration events

**Logged To**: `.tmp/logs/recovery.log`

**Sample Entry**:
```json
{
  "timestamp": "2026-02-13T21:20:00+05:00",
  "corruption_type": "json_parse_error",
  "affected_file": "agents/_registry.json",
  "recovery_strategy": "backup_restore",
  "recovery_success": true,
  "data_loss": false
}
```

---

## User Responsibilities

### Manual Backups

**System Does NOT**:
- Auto-backup entire workspace
- Version control files
- Off-site snapshots

**User Must**:
- Use Git for version control (recommended)
- Periodically copy workspace elsewhere
- Monitor disk health

---

### Disk Maintenance

**User Responsibilities**:
- Ensure adequate disk space
- Monitor for disk errors
- Replace failing hardware

**System:**
- Detects low disk space
- Warns user if < 100 MB free
- Halts writes if < 10 MB free

---

## Summary

Corruption recovery ensures:
- **Automatic Recovery**: JSON backups, file regeneration
- **Graceful Degradation**: Non-critical data loss acceptable
- **User Notification**: Transparency on data loss
- **Prevention Focus**: Atomic writes, validation
- **Critical Protection**: Architecture files immutable
- **Offline Compatible**: No cloud recovery dependencies
