# Link Verification Protocol

> **Purpose**: Define conceptual verification workflows for system readiness  
> **Derived From**: B.L.A.S.T. Phase 2 (Link) + Offline-First Constraints  
> **Status**: Link Phase — Verification Placeholders

---

## Core Principle

**Link phase establishes verification protocols** to ensure the system is ready for execution. Since Omni-Nexus is offline-first, "linking" means validating local environment readiness, not external service connections.

---

## Verification Categories

### 1. Local Dependency Checks

**Purpose**: Verify Python runtime and standard library availability

**Verification Points**:
- Python version compatibility (3.8+)
- Standard library modules accessible (json, pathlib, sys, shutil, datetime)
- File system permissions (read/write to workspace)
- Operating system compatibility (Windows, Linux, macOS)

**Conceptual Workflow**:
```
1. Check Python version
   - Execute: python --version
   - Validate: >= 3.8

2. Import standard library modules
   - Try: import json, pathlib, sys, shutil, datetime
   - Catch: ImportError → report missing dependency

3. Test workspace permissions
   - Create: .tmp/test.txt
   - Write: "test"
   - Read: verify content
   - Delete: cleanup
   - If any fails → report permission error

4. Return readiness report
```

**Expected Output**:
```json
{
  "category": "local_dependencies",
  "status": "ready|not_ready",
  "python_version": "3.11.0",
  "required_modules": ["json", "pathlib", "..."],
  "missing_modules": [],
  "filesystem_writable": true,
  "errors": []
}
```

---

### 2. Filesystem Integrity Verification

**Purpose**: Validate A.N.T. directory structure and core files exist

**Verification Points**:
- All required directories exist (19 total from diagnostics)
- Core memory files present (`task_plan.md`, `progress.md`, `findings.md`, `gemini.md`)
- Architecture directory read-only (post-Blueprint)
- Temporary directories writable (`.tmp/`)

**Conceptual Workflow**:
```
1. Check required directories
   For each in [architecture/, navigation/, tools/, agents/, cli/, .tmp/, ...]:
     - Verify exists
     - Verify is directory
     - Log status

2. Check core files
   For each in [task_plan.md, progress.md, findings.md, gemini.md]:
     - Verify exists
     - Verify is readable
     - Verify non-empty
     - Log status

3. Check architecture immutability
   - Test: attempt write to architecture/test.txt
   - Should fail OR succeed but warn (enforcement level)
   - Log immutability status

4. Check temp directory write access
   - Create: .tmp/write_test.json
   - Write: {"test": "data"}
   - Read: verify
   - Delete: cleanup
   - Log write access status

5. Return integrity report
```

**Expected Output**:
```json
{
  "category": "filesystem_integrity",
  "status": "healthy|degraded|error",
  "directories": {
    "required": 19,
    "found": 19,
    "missing": []
  },
  "core_files": {
    "required": 4,
    "found": 4,
    "missing": []
  },
  "architecture_immutable": true,
  "temp_writable": true
}
```

---

### 3. Schema Validation Workflow

**Purpose**: Verify all data schemas are loadable and validator functional

**Verification Points**:
- `gemini.md` contains valid schema definitions
- Validator tool can parse schema definitions
- All schema types loadable (agent_config, tool_execution, routing_decision)
- Sample payloads validate against schemas

**Conceptual Workflow**:
```
1. Load gemini.md
   - Read architecture/core/gemini.md
   - Parse schema definitions (conceptual - not JSON, but documented)
   - Verify all required schemas present

2. Test schema definitions
   For each schema type [agent_config, tool_execution, routing_decision]:
     - Load schema rules from data_schemas.md
     - Create sample valid payload
     - Validate sample passes
     - Create sample invalid payload
     - Validate sample fails
     - Log validation results

3. Test validator availability
   - Verify tools/core/validator.py exists (if Architect phase complete)
   - Test validator import succeeds
   - Test validate() function callable
   - Log validator status

4. Return schema readiness report
```

**Expected Output**:
```json
{
  "category": "schema_validation",
  "status": "ready|not_ready",
  "schemas_defined": ["agent_config", "tool_execution", "routing_decision"],
  "validator_available": true,
  "validation_tests": {
    "agent_config": {"valid": true, "invalid": true},
    "tool_execution": {"valid": true, "invalid": true},
    "routing_decision": {"valid": true, "invalid": true}
  }
}
```

---

### 4. Agent Registry Readiness

**Purpose**: Verify agent registry initialized and operational

**Verification Points**:
- `agents/_registry.json` exists
- Registry file has valid JSON structure
- Registry schema matches specification
- Registry is writable (atomic write pattern)
- Registry backup mechanism functional

**Conceptual Workflow**:
```
1. Check registry file exists
   - Path: agents/_registry.json
   - Verify exists
   - Verify readable

2. Validate registry structure
   - Read content
   - Parse JSON
   - Verify required fields: {"agents": [], "last_updated": "...", ...}
   - Verify each agent entry has: agent_id, name, type, path, status

3. Test registry write access
   - Create backup: agents/_registry.json.bak
   - Write test entry to temp registry
   - Validate write succeeds
   - Atomic move test (if possible)
   - Restore original
   - Log writability

4. Test backup mechanism
   - Verify .bak file creation possible
   - Test backup restore workflow
   - Log backup readiness

5. Return registry readiness report
```

**Expected Output**:
```json
{
  "category": "agent_registry",
  "status": "ready|not_ready",
  "registry_exists": true,
  "registry_valid_json": true,
  "registry_writable": true,
  "backup_functional": true,
  "agent_count": 0,
  "errors": []
}
```

---

## Verification Orchestration

### Sequential Verification Order

```
1. Local Dependencies (CRITICAL)
   ↓ If ready
2. Filesystem Integrity (CRITICAL)
   ↓ If healthy
3. Schema Validation (IMPORTANT)
   ↓ If ready
4. Agent Registry (IMPORTANT)
   ↓ All complete
5. System Ready for Architect Phase
```

**Halt Conditions**:
- If Local Dependencies not ready → HALT (cannot proceed)
- If Filesystem Integrity error → HALT (cannot proceed)
- If Schema Validation not ready → WARN (can proceed with caution)
- If Agent Registry not ready → WARN (can initialize)

---

## Verification Execution (Conceptual)

### Manual Verification (v1.0)

**User Command** (future):
```bash
python cli/main.py verify-system
```

**Output**:
```
[●] Running system verification...

[✓] Local Dependencies: READY
    Python 3.11.0 ✓
    Required modules: ✓
    Filesystem writable: ✓

[✓] Filesystem Integrity: HEALTHY
    Directories: 19/19 ✓
    Core files: 4/4 ✓
    Architecture immutable: ✓

[✓] Schema Validation: READY
    Schemas defined: 3/3 ✓
    Validator available: ✓

[✓] Agent Registry: READY
    Registry exists: ✓
    Valid structure: ✓
    Writable: ✓

[✓] System Ready for Execution
```

---

### Automated Verification (Future)

**Integration Points**:
- Run on `python cli/main.py init`
- Run before agent spawn
- Run before workflow execution
- Run on system startup

**Not in v1.0 scope** — verification currently manual/conceptual

---

## Offline-First Verification Constraints

### No External Checks

**Prohibited**:
- ❌ Network connectivity tests
- ❌ External API pings
- ❌ DNS resolution checks
- ❌ Cloud service authentication

**Allowed**:
- ✅ Local file existence checks
- ✅ Python import tests
- ✅ File system permission tests
- ✅ JSON parsing validation

---

### Deterministic Verification

**Requirements**:
- Same system state = same verification results
- No timestamp-based checks (except for logs)
- No random test data
- Reproducible error detection

---

## Verification vs Execution Separation

### Link Phase Scope

**Link Phase Defines**:
- What to verify
- How to verify conceptually
- Expected outputs
- Readiness criteria

**Link Phase Does NOT**:
- Implement verification tools (Architect phase)
- Execute verification logic (Architect phase)
- Modify system files
- Create executable code

---

### A.N.T. Architecture Compliance

**Verification placement**:
- Verification **logic** → Tools layer (if implemented)
- Verification **orchestration** → Navigation layer (future)
- Verification **documentation** → Architecture layer (this SOP)

**Current State**:
- Architecture layer: Documentation complete ✓
- Tools layer: Verification tool (future - Architect phase)
- Navigation layer: Verification routing (future - Architect phase)

---

## Integration with Error Recovery

### Verification Failures Trigger Recovery

**If verification fails**:
1. Error recovery protocol activated
2. Attempt auto-fix (if possible):
   - Missing directory → create
   - Missing file → initialize from template
   - Invalid JSON → restore from backup
3. Re-run verification
4. If still fails → user notification

**Linked to**: `error_recovery_protocol.md`

---

## Readiness Criteria Summary

### System Ready If

- ✅ Python 3.8+ available
- ✅ Required directories exist
- ✅ Core files present and readable
- ✅ Schema definitions documented
- ✅ Agent registry initialized

### System Not Ready If

- ❌ Python version incompatible
- ❌ Critical directories missing
- ❌ Core files missing/unreadable
- ❌ File system not writable

---

## Phase Transition

### Link → Architect

Once verification protocol documented:
- Blueprint defines structure
- Link defines readiness checks
- **Architect implements verification tools**
- Architect creates execution logic

**Next Step**: Implement verification as tools in Architect phase

---

## Summary

Link verification ensures:
- **Local Readiness**: Python runtime and dependencies
- **Structural Integrity**: Directory tree and core files
- **Data Validity**: Schema definitions and registry
- **Execution Safety**: Writable temp space, immutable architecture
- **Offline Operation**: No external dependency checks
- **A.N.T. Compliance**: Documentation layer only, no execution
