# AST Usage Patterns

## Purpose
Defines the rules for leveraging Python's built-in Abstract Syntax Tree (`ast`) module when building new Core Verifiers or Diagnostic Scripts to prevent arbitrary code execution and ensure offline capability.

## Structural Overview
The Omni-Nexus strictly relies on Python's `ast` for profound structural checks (e.g., the `python_syntax_check.py` validator).

## Interaction Model
- **Read-Only**: The `ast.parse()` command is invoked upon UTF-8 encoded file string reads. Modifying the AST tree dynamically is explicitly out-of-bounds for current dormant system versions.
- **Reporting Offsets**: All AST walking algorithms (e.g., traversing `ast.FunctionDef`, `ast.Import`) must map their findings strictly to source-code line numbers and offsets to give accurate JSON `code_snippet` readouts to the UI Renderer.

## Future Stability Notes
The `ast` module represents the pinnacle of offline-first diagnostics. While slower over extremely vast codebases than heavily compiled C-linters like `ruff`, sticking to pure `ast` guarantees standard library compatibility on any OS. If performance ever becomes a genuine bottleneck (taking >30s for a validation pipeline), only then will a compiled binary linter be considered an authorized B.L.A.S.T. upgrade.
