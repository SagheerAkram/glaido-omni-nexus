# Workspace Hygiene Check — Specification

> **Purpose**: Enforce strict file placement and directory structure constraints to prevent architectural drift.
> **Phase**: Link (Phase 2) Implementation Target
> **Criticality**: Low (Read-Only)

---

## 1. Objective

The **Workspace Hygiene Validator** ensures that the project root and key directories remain clean and organized. As the codebase grows, there is a risk of "file sprawl" where scripts, logs, or config files are dropped in the root directory or incorrect subdirectories. This tool programmatically enforces the **A.N.T. Layer Separation** (Invariant #2) and **Workspace Isolation** (Invariant #7).

---

## 2. Invariants Enforced

*   **Invariant #2 (A.N.T. Layer Separation)**: Ensures Architecture, Navigation, and Tools remain in their dedicated directories.
*   **Invariant #7 (Workspace Isolation)**: Ensures temporary files and outputs are confined to `.tmp/` and do not pollute the root.
*   **Invariant #4 (File-Based Persistence)**: Verifies that no rogue state files are created outside designated areas.

---

## 3. Validation Logic

### 3.1. Root Directory Purity
The tool must scan the workspace root (`.`) and verify that **only** the following entries exist:

**Allowed Directories**:
*   `.git/`
*   `.tmp/`
*   `agents/`
*   `architecture/`
*   `cli/`
*   `config/`
*   `navigation/`
*   `tests/`
*   `tools/`

**Allowed Files (Exact Match)**:
*   `.gitignore`
*   `LICENSE`
*   `README.md`
*   `progress.md` (System Status)
*   `gemini.md` (Knowledge Base)
*   `task.md` (Active Task State - *Note: If located in root*)
*   `findings.md` (Research Logs)
*   `task_plan.md` (Legacy Plan)

**Allowed File Patterns**:
*   `*.md` (Markdown documentation is allowed in root for developer accessibility, but specific known files are preferred)

**Prohibited**:
*   Any `.py`, `.js`, `.sh` script in root.
*   Any `.json`, `.yaml`, `.xml` config file in root (must be in `config/`).
*   Any `__pycache__` in root.

### 3.2. Architecture Directory Integrity
The `architecture/` directory is for documentation **integrity**.
*   **Rule**: `architecture/` must contain *only* directories.
*   **Rule**: Files within `architecture/` root are allowed only if strictly necessary (e.g. `README.md`).

### 3.3. Tool Directory Structure
The `tools/` directory is the **Engine Room**.
*   **Rule**: `tools/` must contain `core/` and other category directories.
*   **Rule**: `tools/*.py` is **allowed** (utility scripts) but discouraged in favor of `tools/core/`.

---

## 4. Output Schema

The tool must output a JSON object adhering to the standard verification schema.

### 4.1. Success Output
```json
{
  "category": "workspace_hygiene",
  "status": "ready",
  "timestamp": "2026-02-19T21:45:00+05:00",
  "results": {
    "root_clean": true,
    "architecture_clean": true,
    "violations": []
  },
  "message": "Workspace hygiene metrics within limits."
}
```

### 4.2. Failure Output
```json
{
  "category": "workspace_hygiene",
  "status": "error",
  "timestamp": "2026-02-19T21:45:00+05:00",
  "results": {
    "root_clean": false,
    "architecture_clean": true,
    "violations": [
      {
        "location": "root",
        "path": "test_script.py",
        "rule": "No .py files in root"
      },
      {
        "location": "architecture",
        "path": "architecture/TODO.txt",
        "rule": "Only .md files allowed in architecture/"
      }
    ]
  },
  "message": "Workspace hygiene violations detected: 2 issues found.",
  "actionable": true,
  "remediation": "Move 'test_script.py' to tools/ or tests/. Remove 'TODO.txt' or convert to Markdown."
}
```

---

## 5. Constraint Checklist

*   [ ] **Offline-First**: Must use `os` and `pathlib` only. No network.
*   [ ] **Read-Only**: The tool **MUST NOT** delete or move files automatically. It only reports violations.
*   [ ] **Fast**: Execution time must be < 100ms.
*   [ ] **Deterministic**: Verification result depends strictly on file existence.

---

## 6. Future Expansion
*   Adding `__init__.py` enforcement for package discoverability.
*   Enforcing `file_headers` in Python scripts.
