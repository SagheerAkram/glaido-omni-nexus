# Verification Pipeline Anatomy

## Purpose
This document outlines the anatomical structure of the verification pipeline in the Glaido Omni-Nexus. It maps the end-to-end journey of a verification request, detailing how diagnostic tools are aggregated, executed, and rendered without violating offline-first or deterministic axioms.

## Structural Overview
The pipeline consists of three primary phases encapsulated within a single execution sweep:
1. **Registry & Discovery**: The `verification_orchestrator.py` scans a predefined list of trusted tools within `tools/core/`.
2. **Homogeneous Execution**: Each tool is executed sequentially via `subprocess`. The pipeline captures the standardized JSON emitted by each tool to `stdout`.
3. **Structured Rendering**: The raw JSON arrays are passed to `cli/display/verification_renderer.py`, which formats the output into clean, terminal-friendly tables and alert banners using Unicode and ANSI color fallbacks.

## Interaction Model
- The CLI (`cli/main.py`) acts as the user-facing trigger `python cli/main.py verify`.
- The CLI delegates directly to the Verification Orchestrator.
- The Orchestrator spawns tools in isolation. If a tool crashes or hangs, the Orchestrator catches the error, wraps it in a synthetic JSON payload, and continues.
- The formatted output is pushed back up to the CLI for the user, alongside a process exit code indicating overall health (`0` for perfectly healthy, `1` for any failure).

## Future Stability Notes
The verification pipeline is currently synchronous. Future enhancements may explore parallel execution of safe tools, but only if determinism can be absolutely guaranteed. Any new tool added must strictly output JSON matching the `verification_output_format.md` contract.
