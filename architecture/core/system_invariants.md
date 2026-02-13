# System Invariants — Glaido Omni-Nexus

> **Status**: Blueprint Phase — Architecture Layer 1  
> **Updated**: 2026-02-13T20:58:39+05:00

---

## 🔒 IMMUTABLE ARCHITECTURAL RULES

These invariants **MUST NEVER** be violated. Violations trigger self-annealing repair loops.

### 1. Offline-First Design
- **Rule**: System operates with **zero** external dependencies by default
- **Enforcement**: All tools must function without network access
- **Exception**: Future integrations (GitHub API, LLM connectors) remain **disabled** until explicitly activated
- **Validation**: Tool execution must succeed even with network disconnected

### 2. A.N.T. Layer Separation
- **Rule**: 
  - `architecture/` = Documentation only (markdown, JSON schemas)
  - `navigation/` = Thin orchestration (no heavy logic)
  - `tools/` = All executable logic
- **Enforcement**: Navigation layer **NEVER** contains business logic
- **Violation Example**: `navigation/task_router.py` performing data transformation (forbidden)
- **Correct Pattern**: Navigation routes to `tools/data/transform.py` which performs transformation

### 3. Schema-First Data Contracts
- **Rule**: All data structures defined in `gemini.md` **before** implementation
- **Enforcement**: No tool may process undefined schemas
- **Source of Truth**: `gemini.md` JSON schemas are canonical
- **Validation**: Tools must validate input against schemas

### 4. File-Based Persistence
- **Rule**: Local filesystem is the only persistence layer
- **Storage Locations**:
  - Runtime data → `.tmp/`
  - Agent definitions → `agents/[agent_id]/`
  - Logs → `.tmp/logs/`
  - Session state → `.tmp/sessions/`
- **No External Databases**: PostgreSQL, MongoDB, etc. are forbidden

### 5. Deterministic Execution
- **Rule**: Same input **always** produces same output
- **Enforcement**: Tools must be pure functions where possible
- **Logging**: Side effects (file writes, logs) are the only allowed non-determinism
- **Testing**: All tools must be unit testable with predictable results

### 6. Explicit User Consent for Destructive Actions
- **Rule**: Deletion, overwrite, or modification of user data requires **explicit confirmation**
- **Implementation**: CLI tools must use `--force` or `--confirm` flags
- **Forbidden**: Silent deletion or overwriting
- **Example**: `agent.py delete --agent-id=foo` must fail with error. Requires `--confirm` flag.

### 7. Self-Annealing Repair Loop
- **Rule**: Tool failures trigger automatic repair and SOP updates
- **Process**:
  1. Detect failure
  2. Capture error context
  3. Patch script
  4. Retest
  5. Update `architecture/` SOP
- **Tracking**: All repairs logged in `findings.md` → Self-Annealing Learnings

### 8. Brand Identity Consistency
- **Rule**: All CLI output uses brand colors via ANSI escape codes
- **Colors**:
  - Lime Green: `#BFF549` → `\033[38;2;191;245;73m`
  - White: `#FFFFFF` → `\033[38;2;255;255;255m`
  - Black: `#000000` → `\033[38;2;0;0;0m`
- **Enforcement**: CLI tools must import from `cli/display/formatter.py`
- **Tone**: Professional, deterministic, cyberpunk enterprise

### 9. Linear Verification Pipeline
- **Rule**: Verification pipeline must remain linear until post-Stylize expansion approval
- **Current Implementation**: Single orchestrator with fixed sequential tool execution
- **Forbidden**: Parallel execution, conditional skipping, decision trees, retry mechanisms
- **Rationale**: Maintains Navigation layer simplicity and ensures deterministic verification behavior
- **Approval Required**: Any expansion beyond linear model requires explicit architectural approval

### 10. Stylize Phase Separation
- **Rule**: Stylize phase defines presentation contracts only; execution logic must remain unchanged until Trigger phase
- **Documentation Scope**: CLI branding, display contracts, formatting specifications
- **Forbidden During Stylize**: Modifying tools, navigation code, agents, or CLI runtime
- **Rationale**: Separates presentation layer definition from implementation, maintains A.N.T. isolation
- **Implementation Phase**: Trigger (Phase 5) applies Stylize specifications to execution layers

### 11. Operational Hardening Constraint
- **Rule**: Operational hardening may refine documentation and display behavior but must not alter verification execution flow
- **Permitted Changes**: Logging specifications, error messaging, display guidelines, operational behavior documentation
- **Forbidden Changes**: Tool execution logic, orchestrator sequencing, retry mechanisms, execution branching
- **Rationale**: Strengthens system stability through refined operational understanding without expanding system scope
- **Enforcement**: All operational hardening must be documentation-only until explicit Architecture expansion approval

### 12. Expansion Readiness Requirement
- **Rule**: Expansion may begin only when Expansion Readiness Matrix conditions are satisfied and explicitly approved
- **Mandatory Criteria**: All B.L.A.S.T. phases complete, all untouchable invariants enforced, verification operational, documentation current, user approval obtained
- **Forbidden**: Ad-hoc feature additions, scope creep, skipping B.L.A.S.T. phases
- **Rationale**: Prevents uncontrolled system growth while preserving massive architecture scalability
- **Enforcement**: All expansion proposals must pass readiness checklist in `architecture/specifications/expansion_readiness_matrix.md`

---

## 🛡️ ENFORCEMENT MECHANISMS

### Protocol 0 Freeze
- No executable code until Discovery Questions answered ✅
- No tools until architecture/ SOPs exist
- Folder structure may exist but remains empty of logic

### Runtime Validation
- Tools validate input schemas against `gemini.md`
- Navigation layer validates routing decisions
- CLI validates user confirmation for destructive actions

### Self-Correction
- Failures update `findings.md` → Self-Annealing Learnings
- SOPs updated to prevent recurrence
- System learns from errors deterministically

---

**Last Updated**: 2026-02-13T20:58:39+05:00  
**Status**: Active — enforced across all layers
