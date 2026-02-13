# Verification Operational Guidelines

> **Purpose**: Define operational behavior of the verification system under various conditions  
> **Derived From**: Phase 5 Trigger activation, system_invariants.md (linear verification)  
> **Phase**: 5.5 (Operational Hardening)  
> **Status**: Documentation-Only  
> **Created**: 2026-02-13T22:10:00+05:00

---

## Core Principle

The verification system operates in a **deterministic, linear, fail-fast** manner. Operational hardening refines documentation and display behavior without altering execution flow.

---

## Expected Behavior by Verification State

### All Checks Pass (Status: READY)

**System Behavior**:
- Orchestrator returns `overall_status: "ready"`
- CLI exits with code `0`
- Display renders success state with green banner

**Expected Output**:
```
╔════════════════════════════════════════════╗
║    SYSTEM VERIFICATION COMPLETE            ║
╚════════════════════════════════════════════╝

Overall Status: READY
System Ready: Yes

[Table of component statuses]

[✓] System is operational and ready for use
```

**User Action**: None required, proceed with system operation

**Logging**: INFO level
- Log entry: "Verification completed successfully"
- Location: `.tmp/logs/verification.log`

---

### Some Checks Fail (Status: NOT_READY)

**System Behavior**:
- Orchestrator returns `overall_status: "not_ready"`
- CLI exits with code `1`
- Display renders failure state with error banner
- **Orchestrator continues executing all checks** (no short-circuit)

**Expected Output**:
```
╔════════════════════════════════════════════╗
║    SYSTEM VERIFICATION FAILED              ║
╚════════════════════════════════════════════╝

Overall Status: NOT READY
System Ready: No
Critical Failures: N

[Detailed error breakdown]

Required Actions:
  • [Specific remediation steps]

[✗] Resolve errors before proceeding
```

**User Action**: 
1. Review failure details
2. Execute remediation steps
3. Re-run `python cli/main.py verify`

**Logging**: ERROR level
- Log entry: "Verification failed: [component] - [reason]"
- Include full error context
- Location: `.tmp/logs/verification.log`

---

### Degraded State (Status: DEGRADED)

**Current Status**: Not implemented (reserved for post-expansion)

**Future Behavior** (post-expansion only):
- Some components healthy, some degraded but operational
- System can run with reduced capabilities
- Display renders warning state with yellow banner
- CLI exits with code `0` (operational)

**Expansion Requirements**:
- Architecture approval for degraded state definition
- Tool modifications to emit "degraded" status
- Display contract update for warning state rendering

**Current Enforcement**: All tools emit binary ready/error only

---

## Logging Severity Rules

### INFO Level
**Trigger**: Routine operations, successful completions

**Examples**:
- "Verification started"
- "Running check: local_dependencies"
- "Verification completed successfully"

**Destination**: `.tmp/logs/verification.log`

---

### WARNING Level
**Trigger**: Non-critical issues, degraded performance

**Examples** (post-expansion only):
- "Check completed with warnings: [component]"
- "Non-critical dependency missing"

**Destination**: `.tmp/logs/verification.log`

**Current Status**: Not used (no warning states defined)

---

### ERROR Level
**Trigger**: Critical failures, missing requirements

**Examples**:
- "Check failed: filesystem_integrity - missing directories"
- "Python version requirement not met"
- "Tool execution error: [tool_path]"

**Destination**: `.tmp/logs/verification.log`

**Include**:
- Component name
- Failure reason
- Remediation guidance (if available)

---

### CRITICAL Level
**Trigger**: System-level failures, orchestrator errors

**Examples**:
- "Orchestrator timeout exceeded"
- "Tool execution crashed: [exception]"
- "JSON parse error in tool output"

**Destination**: 
- `.tmp/logs/verification.log`
- `.tmp/logs/system.log`

**Include**:
- Full stack trace
- Execution context
- System state snapshot

---

## Retry Policy

### Current Policy: NONE

**Rationale**: Linear invariant enforcement (system_invariants.md #9)

**Behavior**:
- Each tool executes **exactly once** per verification run
- No automatic retries on failure
- No conditional re-execution logic

**User-Initiated Retry**:
- User must manually re-run `python cli/main.py verify`
- Each run is independent, no statecarryover

---

### Future Expansion: Controlled Retries (Post-Expansion Only)

**Requirements for Enabling Retries**:
1. Architecture approval to relax linear invariant
2. Define retry conditions in specification
3. Implement retry counter in orchestrator
4. Add backoff strategy (if applicable)
5. Log all retry attempts

**Potential Retry Scenarios** (not yet implemented):
- Transient filesystem issues
- Temporary resource unavailability
- Network timeouts (if network checks added)

**Enforcement**: Retry logic MUST NOT be added without explicit Architecture phase documentation

---

## Failure Cascades

### Current Behavior: No Cascades

**Independence**: Each verification tool operates independently
- Filesystem failure does not skip schema validation
- All tools execute regardless of prior failures

**Aggregation**: Orchestrator collects all results before determining overall status

---

### Future Expansion: Dependency-Based Execution (Post-Expansion Only)

**Potential Dependencies** (not yet implemented):
- Schema validation depends on filesystem integrity (validator file must exist)
- Agent registry depends on filesystem integrity (registry file must exist)

**Requirements**:
1. Define dependency graph in Architecture layer
2. Update orchestrator to respect dependencies
3. Add skip logic with clear logging
4. Update display contract for "skipped" state

**Current Enforcement**: All tools always execute, no dependencies enforced

---

## Timeout Handling

### Tool-Level Timeouts

**Current Setting**: 30 seconds per tool (in orchestrator)

**Behavior on Timeout**:
- Orchestrator catches `subprocess.TimeoutExpired`
- Returns error status: `{"status": "error", "error": "Tool execution timeout"}`
- Continues to next tool (no cascade)

**Logging**:
- ERROR level: "Tool timeout: [tool_path] - exceeded 30s"

---

### Orchestrator-Level Timeout

**Current Setting**: 120 seconds total (in CLI)

**Behavior on Timeout**:
- CLI catches timeout exception
- Prints error: "Verification timeout (exceeded 120 seconds)"
- Exits with code `1`

**User Action**: Investigate slow tools, check system performance

---

## Display Behavior Refinements

### Color Usage

**Success**: Lime green (#BFF549)
- Status icons: [✓]
- Headers and labels
- Success indicators

**Error**: White (#FFFFFF) + dim
- Status icons: [✗]
- Error messages
- Critical text

**Info**: Lime green
- Status icons: [●]
- Informational messages

**Consistency**: All colors derived from `cli_branding_guidelines.md`

---

### Table Formatting

**Component Tables**:
- Left-aligned component names
- Center-aligned status indicators
- Left-aligned detail text

**Column Widths**: Auto-calculated based on content

**Row Separator**: Thin horizontal line (─)

---

### Status Icons

**Definitions** (from formatter.py):
- Success: `[✓]` in lime green
- Error: `[✗]` in white
- Warning: `[!]` in white (reserved for post-expansion)
- Info: `[●]` in lime green

**Consistency**: No ad-hoc icons, all defined in formatter module

---

## Future Expansion Hooks

### Post-Expansion Features (Explicitly Marked)

The following features are **reserved for future phases** and require:
1. Architecture specification approval
2. Stylize display contract update
3. Navigation orchestrator modification
4. Tool layer expansion (if applicable)

---

#### 1. Degraded State Handling

**Description**: System operational with reduced capabilities

**Prerequisites**:
- Define "degraded" vs "error" distinction in Architecture
- Update tools to emit degraded status
- Create warning state display contract

**Expansion Phase**: Post-Architect expansion approval

---

#### 2. Retry Logic

**Description**: Automatic retry of failed checks

**Prerequisites**:
- Relax linear invariant in system_invariants.md
- Define retry conditions and limits
- Implement retry counter in orchestrator

**Expansion Phase**: Navigation layer expansion approval

---

#### 3. Dependency-Based Execution

**Description**: Skip checks when dependencies fail

**Prerequisites**:
- Define dependency graph in Architecture
- Update orchestrator with skip logic
- Add "skipped" display state

**Expansion Phase**: Navigation layer complexity approval

---

#### 4. Parallel Execution

**Description**: Run independent checks concurrently

**Prerequisites**:
- Prove tool independence (no shared state)
- Define concurrency limits
- Implement result synchronization

**Expansion Phase**: Performance optimization phase

---

#### 5. Custom Verification Sets

**Description**: User-defined subsets of checks

**Prerequisites**:
- Define verification set schema
- Update CLI to accept set identifier
- Create set configuration storage

**Expansion Phase**: CLI feature expansion approval

---

## Operational Invariants

### Invariant 1: Deterministic Output
**Rule**: Same system state + same verification run = identical output

**Enforcement**:
- No random execution order
- No timestamp-dependent logic (except in logs)
- Consistent formatting rules

---

### Invariant 2: Tool Independence
**Rule**: Verification tools do not communicate or share state

**Enforcement**:
- Each tool runs in isolated subprocess
- No shared files written during verification
- Results aggregated only in orchestrator

---

### Invariant 3: Display Separation
**Rule**: Display layer never influences execution logic

**Enforcement**:
- Renderer parses JSON only after orchestrator completes
- No execution code in presentation modules
- CLI invokes orchestrator first, renders second (strict ordering)

---

### Invariant 4: Linear Execution
**Rule**: Tools execute sequentially in fixed order (per system_invariants.md #9)

**Enforcement**:
- Orchestrator iterates tools in list order
- No conditional branching in execution flow
- No parallelization

**Relaxation**: Requires explicit Architecture approval

---

## Error Remediation Guidance

### Filesystem Integrity Failures

**Common Causes**:
- Missing directories from incomplete initialization
- Incorrect workspace structure

**Remediation**:
1. Review required directories in `architecture/core/directory_structure.md`
2. Create missing directories manually or via init script
3. Re-run verification

**Prevention**: Complete system initialization before verification

---

### Dependency Failures

**Common Causes**:
- Wrong Python version
- Missing stdlib modules (rare)

**Remediation**:
1. Upgrade Python to ≥3.8
2. Verify Python installation completeness
3. Re-run verification

**Prevention**: Use supported Python versions

---

### Schema Validation Failures

**Common Causes**:
- Missing `tools/core/validator.py` module

**Remediation**:
1. Implement validator module per specification
2. Ensure importability
3. Re-run verification

**Prevention**: Complete Architect phase before verification

---

### Registry Failures

**Common Causes**:
- Missing `agents/_registry.json` file
- Invalid JSON format

**Remediation**:
1. Create registry file with valid JSON structure
2. Verify write permissions
3. Re-run verification

**Prevention**: Initialize agent registry during setup

---

## Summary

Verification operational guidelines ensure:
1. **Predictable Behavior**: Clear rules for each verification state
2. **Appropriate Logging**: Severity levels match operational impact
3. **No Silent Failures**: All errors surfaced to user
4. **Expansion Discipline**: Future features explicitly marked and gated
5. **Invariant Preservation**: Core principles (linear execution, determinism) enforced

**Operational Hardening**: Strengthens system stability through refined documentation and display behavior without modifying execution flow.
