# Workspace Hygiene Workflow — Standard Operating Procedure

> **Purpose**: Define the operational lifecycle of the Workspace Hygiene Validator.
> **Phase**: Link (Phase 2) Implementation Target
> **Role**: Architecture Enforcer

---

## 1. Execution Trigger

The Workspace Hygiene Validator is executed automatically by the `verification_orchestrator.py`.

*   **Order**: It should run **EARLY** in the pipeline, likely immediately after `filesystem_integrity`.
*   **Reasoning**: If the workspace is polluted or structurally unsound, other tools might fail or produce unreliable results (e.g., importing a rogue `utils.py` from root).

---

## 2. operational Lifecycle

### 2.1. Initialization
*   The tool does **not** require configuration.
*   It utilizes the `pathlib` module to resolve the workspace root relative to its own location.

### 2.2. Scanning Phase
1.  **Root Scan**: Iterates `pathlib.Path.cwd().iterdir()`.
    *   Compares each entry against the **Allowed List** (defined in Spec).
    *   Flags any unknown file or directory.
2.  **Architecture Scan**: Iterates `pathlib.Path("architecture").iterdir()`.
    *   Flags any non-directory entry (unless allowed `.md`).
3.  **Tool Scan**: Iterates `pathlib.Path("tools").iterdir()`.
    *   Flags any non-directory entry (unless allowed `.py`).

### 2.3. Reporting Phase
*   Constructs a JSON result object.
*   If `violations` list is empty -> Status `ready`.
*   If `violations` list is non-empty -> Status `error` (strict enforcement).

---

## 3. Error Handling

### 3.1. Permission Errors
If the tool lacks read permissions for a directory:
*   **Status**: `error`
*   **Message**: "Permission denied accessing [Directory Name]"
*   **Action**: User must grant read access.

### 3.2. Missing Directories
If a mandated directory (e.g., `tools/`) is missing:
*   **Status**: `error`
*   **Message**: "Critical directory missing: tools/"
*   **Action**: Run `filesystem_integrity` check to restore structure.

---

## 4. Remediation Protocol

### 4.1. Root Pollution
*   **Symptom**: "Unknown file in root: `temp_script.py`"
*   **Fix**: Move the file to `tools/scratch/` (if it exists) or `.tmp/`. Delete if unnecessary.

### 4.2. Misplaced Architecture Files
*   **Symptom**: "File in architecture root: `notes.txt`"
*   **Fix**: Move to `architecture/notes/` or convert to `architecture/notes.md`.

### 4.3. Rogue Tool Scripts
*   **Symptom**: "Script in tools root: `run_all.sh`"
*   **Fix**: Move to `cli/scripts/` or `tools/core/`.

---

## 5. Maintenance
*   **Allowlist Updates**: If new top-level directories are approved (e.g. `docs/`), the **Specification** must be updated first.
*   **Pattern Adjustments**: If `.json` files become allowed in root, update Spec.

---

## 6. Constraints
*   **No Auto-Delete**: The tool must never delete files. It only reports.
*   **No Network**: Zero network calls.
