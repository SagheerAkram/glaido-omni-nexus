# Specification: Python Syntax Validator

> **Status**: Blueprint Phase
> **Created**: 2026-02-19T22:06:03+05:00
> **Target Tool**: `tools/core/python_syntax_check.py`
> **Expansion Cycle**: #3

---

## 1. Overview

The **Python Syntax Validator** is a read-only static analysis tool that verifies the syntactic validity of all Python files in the repository. It uses the standard library's `ast` module to parse code without executing it.

**Goal**: Prevent runtime crashes due to potential syntax errors (Typos, IndentationErrors) before they occur during execution.

---

## 2. Invariant Compliance

| Invariant | Compliance Strategy |
|-----------|---------------------|
| **#1 Offline-First** | Uses standard library `ast` only. No pip install required. |
| **#2 A.N.T. Separation** | Logic in `tools/core/`, executed by Orchestrator. |
| **#3 JSON Contracts** | Emits standard JSON report (see Schema). |
| **#4 Local Ownership** | Runs locally, scans local files only. |
| **#5 Deterministic** | Same file content → Same result always. |
| **#6 No Meta-Execution** | Parses code as data. DOES NOT `exec()` or `import` target files. |

---

## 3. Scope of Verification

**Target Directories**:
- `tools/` (Core logic)
- `navigation/` (Orchestration)
- `cli/` (Entry points)
- `architect_enhanced.py` (Legacy root script)

**Excluded Directories**:
- `__pycache__/`
- `.tmp/`
- `.git/`
- `node_modules/` (if any)

**File Pattern**:
- `*.py`

---

## 4. Verification Logic

1. **Discovery**: Walk target directories to find all `.py` files.
2. **Parsing**: For each file:
   - Read content as UTF-8 string.
   - Attempt `ast.parse(content, filename=file_path)`.
3. **Validation**:
   - **Success**: AST generated without exception.
   - **Failure**: `SyntaxError` or `IndentationError` caught.
4. **Reporting**:
   - Collect all failures (path, line number, error message).
   - Determine overall status.

---

## 5. JSON Output Schema

**Tool Category**: `python_syntax`

```json
{
  "category": "python_syntax",
  "status": "ready" | "error",
  "timestamp": "ISO-8601 string",
  "results": {
    "files_scanned": Integer,
    "issues_found": Integer,
    "scanned_directories": [String],
    "syntax_errors": [
      {
        "file": "Relative Path (e.g., tools/core/validator.py)",
        "line": Integer,
        "column": Integer,
        "message": "Error description (e.g., unexpected indent)",
        "code_snippet": "Context line content (optional)"
      }
    ]
  }
}
```

---

## 6. Failure Conditions

- **Red (Error)**:
  - Any `SyntaxError` found in any file.
  - Any `IndentationError` found in any file.
  - File read permission error (access denied).

- **Green (Ready)**:
  - All files parsed successfully.
  - Zero syntax errors.

---

## 7. Performance Constraints

- **Timeout**: Tool must complete within 10 seconds (for < 1000 files).
- **Memory**: Stream file reading, do not load all files into memory at once.

---

## 8. Security

- **NO EXECUTION**: Explicitly forbidden to use `exec()`, `eval()`, or `importlib` on scanned files.
- **AST ONLY**: Abstract Syntax Tree parsing is safe for effectively all static code.

---

**Last Updated**: 2026-02-19T22:06:03+05:00
**Author**: Antigravity
