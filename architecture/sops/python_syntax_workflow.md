# SOP: Python Syntax Validator Workflow

> **Status**: Blueprint Phase (B)
> **Goal**: Define operational procedure for Python Syntax Validation
> **Expansion Cycle**: #3
> **Created**: 2026-02-19T22:06:03+05:00

---

## 1. Overview

The **Python Syntax Validator** ensures that all Python code in the repository is syntactically valid before any execution attempts. This prevents "crash-on-import" scenarios where a single typo breaks the entire CLI or Orchestrator.

**Core Function**: Static analysis using `ast.parse()`. No code execution.

---

## 2. Integration Point

**Position in Verification Pipeline**:
1. `local_dependencies` (Check Python Version)
2. `workspace_hygiene` (Check file structure)
3. **`python_syntax` (NEW)** — *Validate code structure before checking packages*
4. `filesystem_integrity` (Check missing dirs)
5. `python_packages` (Check dependencies)
6. `schema_validation` (Check logic)
7. `agent_registry` (Check data)

**Rationale**:
- If syntax is invalid, dependency checks might fail with obscure import errors.
- Syntax checking is fast and should fail early.

---

## 3. Execution Lifecycle

1. **Invocation**: Orchestrator calls `tools/core/python_syntax_check.py`.
2. **Setup**: Tool identifies root directory and target folders (`tools/`, `navigation/`, `cli/`).
3. **Scanning**: Recursively finds all `*.py` files.
4. **Analysis**:
   - Reads each file.
   - Parses with `ast`.
   - Catches `SyntaxError` exceptions.
5. **Output**: Generates JSON report.
6. **Orchestrator Action**:
   - If `status: error` → Mark verification as failed.
   - If `status: ready` → Proceed to next tool.

---

## 4. Error Handling

### Syntax Errors
- **Detection**: `SyntaxError`, `IndentationError`
- **Action**: Report file path, line number, and error message.
- **Severity**: BLOCKER (Verification Fails).

### Encoding Errors
- **Detection**: `UnicodeDecodeError`
- **Action**: Report as "Invalid Encoding" (Must be UTF-8).
- **Severity**: BLOCKER.

### Permission Errors
- **Detection**: `PermissionError` (access denied)
- **Action**: Report as "Access Denied".
- **Severity**: BLOCKER.

---

## 5. Remediation Procedures

See `verification_operational_guidelines.md` for detailed user instructions.

**General Fixes**:
1. Open the file at the reported line number.
2. Correct the syntax (missing colon, mismatched parens, bad indentation).
3. Save and re-run `verify`.

---

**Last Updated**: 2026-02-19T22:06:03+05:00
**Author**: Antigravity
