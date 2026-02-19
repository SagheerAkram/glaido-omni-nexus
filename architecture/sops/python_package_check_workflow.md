# SOP: Python Package Validator — Expansion Workflow

> **Purpose**: Define the Standard Operating Procedure for expanding the verification pipeline with the Python Package Validator tool
> **Expansion Candidate**: Extended Verification Tool — Python Package Validator
> **Risk Classification**: LOW RISK
> **B.L.A.S.T. Phase**: Blueprint (B) — Active
> **Created**: 2026-02-19T21:12:39+05:00
> **Gate Authorization**: Approved by user — 2026-02-19T21:12:39+05:00
> **Status**: SOP Defined — Blueprint Phase Only

---

## Expansion Authorization Record

| Field | Value |
|-------|-------|
| **Candidate Name** | Python Package Validator |
| **Registry Entry** | `expansion_candidate_registry.md` |
| **Risk Level** | LOW |
| **Gate State at Authorization** | LOCKED → UNLOCKED |
| **Authorization Timestamp** | 2026-02-19T21:12:39+05:00 |
| **Authorized By** | User approval statement |
| **Current B.L.A.S.T. Phase** | Blueprint (B) |

---

## B.L.A.S.T. Phase Overview

| Phase | Letter | Status | Action |
|-------|--------|--------|--------|
| Blueprint | B | ✅ ACTIVE | Architecture docs — **this phase** |
| Link | L | ⏳ Pending | Create `tools/core/python_package_check.py` |
| Architect | A | ⏳ Pending | Wire tool into orchestrator |
| Stylize | S | ⏳ Pending | CLI display for `python_packages` category |
| Trigger | T | ⏳ Pending | Activate and run full verification |

---

## Phase B — Blueprint (Current Phase)

### Objective

Produce all architecture-level artifacts required before any code is written.

### Required Deliverables

| Artifact | Status |
|----------|--------|
| `architecture/specifications/python_package_check_spec.md` | ✅ Created |
| `architecture/sops/python_package_check_workflow.md` | ✅ Created (this file) |
| Display contract updated (`verification_display_contract.md`) | ✅ Updated |
| Op. guidelines updated (`verification_operational_guidelines.md`) | ✅ Updated |

### Constraints During Blueprint Phase

- ❌ DO NOT create `tools/core/python_package_check.py`
- ❌ DO NOT modify `navigation/orchestrator/verification_orchestrator.py`
- ❌ DO NOT modify `cli/main.py` or any CLI files
- ❌ DO NOT modify `cli/display/verification_renderer.py`
- ✅ Architecture and documentation layer ONLY

### Completion Criterion

Blueprint phase is complete when all four deliverables above are marked ✅ and reviewed.

---

## Phase L — Link (Next Phase)

### Objective

Create the tool implementation and verify standalone execution.

### Actions

1. Create `tools/core/python_package_check.py`
   - Must conform to `python_package_check_spec.md`
   - Must emit valid JSON to stdout
   - Must use `importlib.util.find_spec()` only
   - Must include outer try/except for error JSON emission
2. Test tool standalone: `python tools/core/python_package_check.py`
3. Validate output against `verification_output_format.md`
4. Confirm no network calls via static code review
5. Confirm `find_spec` used, not bare `import`

### Gate Condition

Link phase is complete when standalone tool produces correct JSON for both PASS and FAIL states without violating any invariant.

---

## Phase A — Architect (Wiring Phase)

### Objective

Wire the tool into the verification orchestrator and confirm pipeline integrity.

### Actions

1. Edit `navigation/orchestrator/verification_orchestrator.py`
   - Append to `tools` list at position 5:
     ```python
     ("python_packages", workspace / "tools/core/python_package_check.py"),
     ```
2. Run `python navigation/orchestrator/verification_orchestrator.py` directly
3. Confirm all 5 tools execute in sequence
4. Confirm `overall_status` aggregation is correct
5. Update `architecture/core/expansion_candidate_registry.md` status to "In Progress"

### Gate Condition

Architect phase is complete when 5-tool orchestrator run produces correct aggregated JSON.

---

## Phase S — Stylize (Display Phase)

### Objective

Update the CLI display layer to correctly render the `python_packages` verification category.

### Actions

1. Edit `cli/display/verification_renderer.py`
   - Add `python_packages` case to the category rendering block
   - Display: label "Python Packages", status icon, and missing package list if any
2. Confirm display output matches `verification_display_contract.md §Python Package Validator Display`
3. Confirm no execution logic introduced into renderer

### Gate Condition

Stylize phase complete when `glaido verify` renders `python_packages` correctly in all three states (ready, warning, error).

---

## Phase T — Trigger (Activation Phase)

### Objective

Activate full end-to-end pipeline and mark expansion complete.

### Actions

1. Run full `python cli/main.py verify` end-to-end
2. Confirm exit code 0 when all packages present
3. Confirm exit code 1 when a package is missing (test with a deliberately removed package)
4. Update `architecture/core/expansion_candidate_registry.md` status to "COMPLETE"
5. Update `architecture/core/expansion_gate_state.md` to reflect expansion completed
6. Update `progress.md` with new phase: "Phase 7 — Python Package Validator Expansion"
7. Reset Expansion Gate to LOCKED (dormant) until next candidate proposal

### Gate Condition

Trigger phase complete when:
- All 5 tools run sequentially in `glaido verify`
- Display renders correctly for success and failure states
- All documentation updated to reflect completed expansion

---

## Rollback Procedure

If any phase fails validation:

| Phase Failed | Rollback Action |
|-------------|----------------|
| Link | Delete `tools/core/python_package_check.py`, return to Blueprint |
| Architect | Revert orchestrator to 4-tool list, return to Link |
| Stylize | Revert renderer, return to Architect state |
| Trigger | Revert all phase changes, full re-audit required |

---

## Invariant Verification Checkpoints

At each phase boundary, confirm:

| Check | Method |
|-------|--------|
| No network calls added | Static code grep for `urllib`, `requests`, `socket` |
| A.N.T. separation intact | Tool in `tools/`, orchestrator in `navigation/` |
| JSON output conforms | Compare against `verification_output_format.md` |
| Linear pipeline preserved | Orchestrator uses sequential for-loop (no parallelism) |
| No execution in display | Grep `cli/display/` for `subprocess`, `os.system`, etc. |

---

## Contact and Authority

All phase transitions require:
1. Explicit user direction to begin next phase
2. Completion of all deliverables for the current phase
3. No implicit phase advancement — each phase is a discrete user-approved step

---

**Last Updated**: 2026-02-19T21:12:39+05:00
**Current Phase**: Blueprint (B) — ACTIVE
**Next Phase**: Link (L) — Awaiting user direction
