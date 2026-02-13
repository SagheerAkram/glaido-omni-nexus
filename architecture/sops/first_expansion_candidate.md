# First Expansion Candidate: Extended Verification Tool

> **Purpose**: Define the first controlled expansion candidate for the Glaido Omni-Nexus system  
> **Derived From**: Expansion Readiness Matrix, B.L.A.S.T. Protocol, System Invariants  
> **Phase**: 6.1 (Expansion Approval Preparation)  
> **Status**: Proposal — Awaiting user approval  
> **Created**: 2026-02-13T22:20:00+05:00

---

## Proposed Expansion

**Feature Name**: Extended Verification Tool — Python Package Validator

**Category**: Verification Tool (read-only, offline)

**Purpose**: Verify that required Python packages are available in the local Python environment

**Risk Level**: **LOW RISK** (under Expansion Readiness Matrix criteria)

---

## Feature Specification

### Tool Name
`tools/core/python_package_check.py`

### Functionality
1. Read a manifest of required Python packages (e.g., `requirements.txt` or embedded list)
2. Attempt to import each package using Python's `importlib`
3. Record which packages are present vs. missing
4. Emit standardized JSON output conforming to `verification_output_format.md`

### Example Output
```json
{
  "category": "dependency",
  "status": "ready|error",
  "timestamp": "2026-02-13T22:20:00+05:00",
  "results": {
    "packages_checked": 5,
    "packages_present": 4,
    "packages_missing": 1,
    "details": [
      {"name": "pathlib", "status": "present", "version": "built-in"},
      {"name": "json", "status": "present", "version": "built-in"},
      {"name": "argparse", "status": "present", "version": "built-in"},
      {"name": "subprocess", "status": "present", "version": "built-in"},
      {"name": "hypothetical_package", "status": "missing", "version": null}
    ]
  },
  "message": "1 package missing",
  "actionable": true,
  "remediation": "Install missing packages: pip install hypothetical_package"
}
```

### User Experience
When running `python cli/main.py verify`, the output will include:

**Success State** (all packages present):
```
[✓] Python Packages: All required packages available (5/5)
```

**Failure State** (packages missing):
```
[✗] Python Packages: Missing required packages (4/5)
    • hypothetical_package — not installed
    → Install: pip install hypothetical_package
```

---

## Risk Classification: LOW RISK

### Why This Is Low Risk

**Follows Existing Patterns**:
- Mirrors the structure of `local_dependency_check.py`, `filesystem_integrity_check.py`
- Uses same JSON output schema
- Integrates into orchestrator with minimal changes (add to tool list)

**Read-Only Operation**:
- Only **reads** package availability via `importlib.import_module()`
- Does not install, uninstall, or modify packages
- No filesystem writes beyond standard logging

**Offline-Compatible**:
- Uses local Python environment only
- No network calls, no PyPI queries
- Works entirely offline

**Deterministic**:
- Same Python environment → same output
- No random behavior, no timestamps in logic (only in logs)

**No Orchestrator Logic Changes**:
- Orchestrator simply adds this tool to the list
- Execution remains linear, sequential
- No new branching, conditional logic, or retries

**Clear Failure Modes**:
- Package present → success
- Package missing → failure with clear remediation
- Import error → handled gracefully, logged

**Minimal Complexity**:
- ~50-80 lines of code
- Single file, no dependencies beyond stdlib
- Easy to test, easy to verify

---

## Invariant Preservation Analysis

### Invariant #1: Offline-First Constraint ✅

**Requirement**: All features work offline

**Compliance**:
- Tool uses `importlib.import_module()` which operates on local Python environment
- No network calls, no external API dependencies
- Package availability determined by local interpreter state
- Works identically with or without internet connection

**Verification**: Run tool on air-gapped machine → identical behavior

---

### Invariant #2: A.N.T. Layer Separation ✅

**Requirement**: Tools in Tools layer, routing in Navigation, specs in Architecture

**Compliance**:
- **Tool**: `tools/core/python_package_check.py` (Tools layer)
- **Orchestration**: `verification_orchestrator.py` adds tool to list (Navigation layer)
- **Specification**: This SOP + JSON schema (Architecture layer)
- **Presentation**: Renderer parses JSON, applies display contract (Trigger layer)

**No layer mixing**: Tool emits JSON, orchestrator aggregates, renderer displays

**Verification**: Code review confirms no presentation logic in tool, no execution logic in renderer

---

### Invariant #3: JSON Data Contracts ✅

**Requirement**: All tools emit JSON conforming to schema

**Compliance**:
- Output conforms to `verification_output_format.md` schema
- Required fields: `category`, `status`, `timestamp`, `results`, `message`, `actionable`, `remediation`
- Schema-validated by orchestrator (future enhancement)

**Verification**: Parse tool output with JSON schema validator

---

### Invariant #4: Local Execution Ownership ✅

**Requirement**: User controls all execution, no background tasks

**Compliance**:
- Tool runs only when `verify` command invoked
- No daemon processes, no scheduled tasks, no automatic triggers
- Exits cleanly after emitting JSON

**Verification**: Process monitoring shows tool spawns and exits only during verify runs

---

### Invariant #5: Deterministic Automation ✅

**Requirement**: Same input → same output

**Compliance**:
- Same Python environment → same package availability → same results
- No random behavior, no non-deterministic algorithms
- Timestamps only in logs, not in logic

**Verification**: Run tool twice in identical environment → identical JSON output (excluding timestamp)

---

### Invariant #6: No Meta-Execution ✅

**Requirement**: Tools execute domain logic, not self-modification

**Compliance**:
- Tool checks package availability only
- Does not modify Python environment
- Does not install/uninstall packages
- Does not write to `tools/` directory
- No use of `exec()`, `eval()`, or dynamic code generation

**Verification**: Code review confirms no filesystem writes to tools/, no package installation calls

---

### Invariant #7: Workspace Isolation ✅

**Requirement**: All operations scoped to workspace

**Compliance**:
- Reads package list from workspace (if using `requirements.txt`)
- Logs to `.tmp/logs/` within workspace
- Does not modify global Python installation
- Does not modify system environment variables

**Verification**: Run tool → confirm no modifications outside workspace root

---

### Invariant #10: Stylize Phase Separation ✅

**Requirement**: Presentation specs before presentation code

**Compliance**:
- **Stylize Phase** (to be done): Define how package check results display in CLI
  - Update `verification_display_contract.md` with package check rendering rules
  - Specify color coding, table format for package list
- **Trigger Phase** (to be done): Implement display in `verification_renderer.py`
  - Parse `category: "dependency"` and render package details
  - Apply branding per `cli_branding_guidelines.md`

**Workflow**:
1. This SOP approved (Architecture)
2. Stylize contract updated (Presentation spec)
3. Tool implemented (Architect phase)
4. Renderer updated (Trigger phase)

**No Stylize-before-spec violations**

---

### Invariant #11: Operational Hardening Constraint ✅

**Requirement**: Operational behavior documented before deployment

**Compliance**:
- This SOP defines expected behavior, failure modes, remediation
- **Operational Hardening** (to be done): Update `verification_operational_guidelines.md`
  - Add "Python Package Failures" section to error remediation
  - Define logging severity for package missing vs import error
  - Document user actions for package installation

**No deployment before operational guidelines exist**

---

### Invariant #12: Expansion Readiness Requirement ✅

**Requirement**: Expansion Readiness Matrix criteria satisfied

**Compliance**:
- ✅ All B.L.A.S.T. phases complete (0-5.5)
- ✅ All untouchable invariants enforced
- ✅ Verification operational
- ✅ Documentation current
- ⚠️ User approval pending (this SOP serves as approval request)

**Gate Status**: Ready for user approval

---

## Integration into Linear Verification Pipeline

### Current Orchestrator Structure

```python
# navigation/orchestrator/verification_orchestrator.py (simplified)

def verify_system():
    tools = [
        workspace / "tools/core/local_dependency_check.py",
        workspace / "tools/core/filesystem_integrity_check.py",
        workspace / "tools/core/schema_validator_stub.py",
        workspace / "tools/agents/registry_readiness_check.py",
    ]
    
    results = []
    for tool in tools:
        result = run_verification_tool(tool)
        results.append(result)
    
    # Aggregate and return JSON
    return aggregate_results(results)
```

### Post-Expansion Structure

```python
# navigation/orchestrator/verification_orchestrator.py (updated)

def verify_system():
    tools = [
        workspace / "tools/core/local_dependency_check.py",
        workspace / "tools/core/filesystem_integrity_check.py",
        workspace / "tools/core/python_package_check.py",  # NEW TOOL
        workspace / "tools/core/schema_validator_stub.py",
        workspace / "tools/agents/registry_readiness_check.py",
    ]
    
    results = []
    for tool in tools:
        result = run_verification_tool(tool)
        results.append(result)
    
    # Aggregate and return JSON
    return aggregate_results(results)
```

### Key Integration Points

**1. Orchestrator Modification (Navigation Layer)**
- **Change**: Add tool path to `tools` list
- **Scope**: 1 line addition
- **Complexity**: Trivial
- **Risk**: None (no logic change, only data)

**2. Renderer Update (Presentation Layer)**
- **Change**: Parse `category: "dependency"` and render package details
- **Scope**: Add conditional block in `_render_failure_state()` and `_render_success_state()`
- **Complexity**: Low (mirror existing rendering patterns)
- **Risk**: None (presentation only)

**3. Display Contract Update (Architecture Layer)**
- **Change**: Add section to `verification_display_contract.md` specifying package check rendering
- **Scope**: ~30 lines documentation
- **Complexity**: Trivial
- **Risk**: None (documentation only)

**4. Operational Guidelines Update (Architecture Layer)**
- **Change**: Add "Python Package Failures" to `verification_operational_guidelines.md`
- **Scope**: ~50 lines documentation
- **Complexity**: Trivial
- **Risk**: None (documentation only)

---

## Execution Flow Preservation

### Linear Execution Maintained

**Before Expansion**:
```
1. local_dependency_check
2. filesystem_integrity_check
3. schema_validator_stub
4. registry_readiness_check
```

**After Expansion**:
```
1. local_dependency_check
2. filesystem_integrity_check
3. python_package_check  ← NEW
4. schema_validator_stub
5. registry_readiness_check
```

**Key Properties**:
- ✅ Still sequential (one tool at a time)
- ✅ Still linear (no branching)
- ✅ Still deterministic (fixed order)
- ✅ No conditional skipping (all tools always run)
- ✅ No retries (each tool runs once)

**Invariant #9 (Linear Verification Pipeline) preserved**

---

### Tool Independence Maintained

**Independence Criteria**:
- ✅ No shared state between tools
- ✅ No inter-tool communication
- ✅ No dependency on prior tool results
- ✅ Isolated subprocess execution per tool

**Package check tool**:
- Reads Python environment state (read-only)
- Emits JSON to stdout
- Exits cleanly
- Does not depend on filesystem check, dependency check, or any other tool

**Operational Invariants preserved**

---

## B.L.A.S.T. Protocol Compliance for Expansion

### Phase 1: Blueprint (Architecture)

**Deliverables**:
- ✅ This SOP: `first_expansion_candidate.md`
- 🔄 Update: `verification_display_contract.md` (add package check rendering)
- 🔄 Update: `verification_operational_guidelines.md` (add package failures section)

**Status**: In progress (this document)

---

### Phase 2: Link (Verification)

**Deliverables**:
- 🔄 Extend: `link_verification_protocol.md` (if needed)
- ✅ No new verification needed (package check verifies itself)

**Status**: Not required (package check is a verification tool)

---

### Phase 3: Architect (Implementation)

**Deliverables**:
- 🔄 Create: `tools/core/python_package_check.py`
- 🔄 Update: `navigation/orchestrator/verification_orchestrator.py` (add tool to list)

**Status**: Pending user approval

---

### Phase 4: Stylize (Presentation Spec)

**Deliverables**:
- 🔄 Update: `verification_display_contract.md` (package check display rules)

**Status**: Pending Architecture approval

---

### Phase 5: Trigger (Presentation Activation)

**Deliverables**:
- 🔄 Update: `cli/display/verification_renderer.py` (render package details)

**Status**: Pending Stylize completion

---

### Phase 6: Operational Hardening

**Deliverables**:
- 🔄 Update: `verification_operational_guidelines.md` (package failure remediation)

**Status**: Pending Trigger completion

---

## Approval Request

### User Decision Required

**Question**: Approve Python Package Validator as the first expansion?

**If Approved**:
1. Proceed with Blueprint phase updates
2. Implement tool in Architect phase
3. Complete full B.L.A.S.T. cycle
4. Deliver functional expansion with full documentation

**If Rejected**:
- System remains dormant
- No expansion occurs
- Alternative candidates can be proposed

---

## Alternative Low-Risk Candidates (For Reference)

If Python Package Validator is rejected, these alternatives are also low-risk:

### Alternative 1: Configuration File Validator
- **Purpose**: Verify `gemini.md` or other config files are valid
- **Risk**: Low (read-only, offline, follows tool pattern)

### Alternative 2: Agent Definition Validator
- **Purpose**: Verify agent JSON files have valid structure
- **Risk**: Low (read-only, offline, follows tool pattern)

### Alternative 3: Log File Integrity Check
- **Purpose**: Verify `.tmp/logs/` directory is writable
- **Risk**: Low (read-only, offline, follows tool pattern)

**Current Recommendation**: Python Package Validator (most immediately useful)

---

## Expected Timeline

**If approved today**:
- Blueprint updates: 1 session
- Tool implementation: 1 session
- Stylize + Trigger: 1 session
- Operational hardening: 1 session
- **Total**: 4 sessions to complete expansion

**Risk of Delay**: None (system remains stable in dormant state while expansion progresses)

---

## Summary

The Python Package Validator is a **textbook low-risk expansion**:
- Follows existing tool patterns exactly
- Preserves all untouchable invariants (#1-7, #10-12)
- Integrates into linear pipeline with 1-line orchestrator change
- No execution flow alterations, only additive tool
- Full B.L.A.S.T. cycle ensures proper documentation

**Recommendation**: Approve as first expansion to demonstrate controlled growth process.

---

**Last Updated**: 2026-02-13T22:20:00+05:00  
**Status**: Awaiting user approval  
**Next Action**: User decision on expansion approval
