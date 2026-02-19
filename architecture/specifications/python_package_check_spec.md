# Python Package Validator — Verification Tool Specification

> **Purpose**: Define the architecture, contracts, and invariant constraints for the Python Package Validator verification tool
> **Expansion Candidate**: Extended Verification Tool — Python Package Validator
> **Risk Classification**: LOW RISK
> **B.L.A.S.T. Phase**: Blueprint (B)
> **Created**: 2026-02-19T21:12:39+05:00
> **Gate Authorization**: Approved by user — 2026-02-19T21:12:39+05:00
> **Status**: Blueprint Specification — No Implementation Yet

---

## Purpose

The Python Package Validator verifies that all Python packages required by the Glaido Omni-Nexus system are importable in the current environment. It complements the existing `local_dependency_check.py` (which checks Python version and stdlib modules) by targeting **installable packages** — those that exist in `site-packages` rather than the standard library.

---

## Invariant Compliance Statement

This tool must comply with all active system invariants:

| Invariant | Rule | Compliance Status |
|-----------|------|-------------------|
| #1 Offline-First | No network calls permitted | ✅ `importlib.util.find_spec()` only |
| #2 A.N.T. Layer Separation | Tool belongs in `tools/core/`, not `navigation/` | ✅ Planned path: `tools/core/python_package_check.py` |
| #3 JSON Contracts | Output must conform to `verification_output_format.md` | ✅ Defined in §Output Contract below |
| #4 Local Execution | CLI-triggered only, no daemon or scheduler | ✅ No self-scheduling |
| #5 Deterministic Output | Same environment → identical output every run | ✅ `importlib` is deterministic |
| #6 No Meta-Execution | No `pip install`, `subprocess pip`, or network fetches | ✅ Strictly read-only |
| #7 Workspace Isolation | Operates within workspace root only | ✅ Package list sourced from local config |
| #10 Stylize Separation | Display contract defined before implementation | ✅ Defined in §Display Contract Extension |
| #11 Op. Hardening | Operational guidelines updated before implementation | ✅ Defined in `verification_operational_guidelines.md` |
| #12 Expansion Ready | Approved via Expansion Gate Authorization | ✅ Gate unlocked 2026-02-19 |

---

## Tool Identity

| Field | Value |
|-------|-------|
| **Tool Name** | Python Package Validator |
| **File Path** | `tools/core/python_package_check.py` (to be created in Link phase) |
| **Category** | `python_packages` |
| **Execution Order** | 5th — appended after existing tool 4 (`agent_registry`) |
| **Timeout Budget** | 15 seconds (well within the 30s per-tool limit) |
| **Priority** | IMPORTANT (non-critical, same tier as schema_validation) |

---

## Input Contract

**No external input accepted.**

The tool reads its package list from a checked-in configuration constant defined internally within the tool. The list is **not** read from any external file, registry, or user argument.

**Package List Source**:
```
Defined as a Python list literal inside the tool:
REQUIRED_PACKAGES = ["json", "pathlib", "importlib", ...]
```

The list must be explicitly maintained and updated only through the B.L.A.S.T. cycle.

---

## Output Contract

Output must be valid JSON conforming to `verification_output_format.md`. The following fields are required:

```json
{
  "category": "python_packages",
  "status": "ready | error",
  "executed": true,
  "checks": {
    "total": <int>,
    "available": <int>,
    "missing": <int>
  },
  "packages": {
    "<package_name>": "available | missing"
  },
  "missing_list": ["<package_name>", ...],
  "timestamp": "<ISO-8601>"
}
```

### Status Rules

| Condition | `status` Value |
|-----------|---------------|
| All packages importable | `"ready"` |
| One or more packages missing | `"error"` |
| `importlib` itself unavailable | `"error"` (with descriptive `error` field) |
| Tool crash / unhandled exception | `"error"` (caught at outer try/except) |

### Orchestrator Compatibility

The orchestrator reads `status` and checks for `"ready"` or `"healthy"`. This tool emits only `"ready"` or `"error"` — both are valid orchestrator inputs per `verification_orchestrator.py` line 103–106.

---

## Execution Model

### Scope

The tool checks only packages listed in `REQUIRED_PACKAGES`. It does **not**:
- Scan all site-packages
- Check version numbers (phase-1 scope only)
- Attempt imports with side effects
- Read `requirements.txt` or `pyproject.toml` (reserved for future expansion)

### Check Mechanism

```
For each package in REQUIRED_PACKAGES:
    Use importlib.util.find_spec(package_name)
    If spec is not None → "available"
    If spec is None → "missing"
```

No `import` statement is executed. `find_spec()` locates the module without executing it, preserving Invariant #6 (no meta-execution side effects).

### Initial Package List (MVP)

The following packages are included in phase-1 scope. All are stdlib or commonly available:

| Package | Tier |
|---------|------|
| `json` | stdlib |
| `pathlib` | stdlib |
| `importlib` | stdlib |
| `subprocess` | stdlib |
| `sys` | stdlib |
| `io` | stdlib |
| `argparse` | stdlib |

> **Note**: External packages (e.g., third-party pip packages) are explicitly out of scope for phase-1. The list MAY be expanded in a future B.L.A.S.T. cycle only.

---

## Failure Classification

| Failure Type | Severity | Orchestrator Impact |
|-------------|----------|---------------------|
| One or more stdlib packages missing | CRITICAL | Contributes to `not_ready` |
| All packages present | PASS | Contributes to `ready` |
| Tool execution timeout | ERROR | Orchestrator marks as `error`, not fatal |
| Unhandled exception | ERROR | Outer try/except emits error JSON |

---

## Integration into Verification Pipeline

### Orchestrator Change (Link Phase Only)

When this tool is activated in the Link phase, the following line is appended to the `tools` list in `verification_orchestrator.py`:

```python
("python_packages", workspace / "tools/core/python_package_check.py"),
```

**This change is explicitly NOT made during Blueprint phase.**

### Execution Order After Integration

1. `local_dependency_check.py` — CRITICAL
2. `filesystem_integrity_check.py` — CRITICAL
3. `schema_validator_stub.py` — IMPORTANT
4. `registry_readiness_check.py` — IMPORTANT
5. `python_package_check.py` — IMPORTANT ← **NEW**

---

## Display Contract Extension

The `verification_display_contract.md` is updated in this Blueprint phase to define presentation rules for `python_packages` category. See §Python Package Validator Display section in that document.

**Display key**: `"python_packages"` maps to label **"Python Packages"** in the renderer.

---

## Constraints: What This Tool Must NEVER Do

| Prohibited Action | Invariant |
|------------------|-----------|
| Execute `pip install` or `pip check` | #6 No Meta-Execution |
| Make any network request | #1 Offline-First |
| Write any file to disk | #7 Workspace Isolation |
| Import packages (only `find_spec`) | #5 Deterministic (prevent side-effect imports) |
| Read `requirements.txt` or external config | #3 JSON Contracts (input must be self-contained) |
| Use `subprocess` to call Python scripts | #4 Local Execution (direct use only) |

---

## Verification Plan (for Link Phase)

When the Link phase begins, the following must be verified before the tool is merged into the orchestrator:

1. **Unit**: Tool outputs valid JSON for both `"ready"` and `"error"` states
2. **Contract**: Output JSON validates against `verification_output_format.md` schema
3. **Invariant #1**: Confirmed no network socket calls via static code review
4. **Invariant #6**: Confirmed `find_spec` used, not bare `import`
5. **Integration**: Orchestrator runs 5 tools in sequence, overall status correct
6. **Display**: `verification_renderer.py` correctly renders `python_packages` category

---

**Last Updated**: 2026-02-19T21:12:39+05:00
**B.L.A.S.T. Phase**: Blueprint Complete — Link Phase Pending
