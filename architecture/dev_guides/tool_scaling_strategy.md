# Tool Scaling Strategy

## Purpose
Details the required patterns to integrate future independent diagnostic and analytical tools gracefully into the system's `tools/` ecosystem without triggering orchestrator strain or dependency hell.

## Structural Overview
As the Glaido Omni-Nexus integrates web scraping, memory management, or database migrations, tools will dramatically multiply. The system forces strict horizontal scaling instead of vertical script bloat.

## Interaction Model
- **Atomic Specificity**: New tools must execute exactly one logical process (e.g. `check_db_schema.py`) rather than generic multipurpose wrappers (`check_all_backends.py`).
- **Standardized Invocation**: Tools are called dynamically. Thus, a new tool dropping into `tools/core/` requires no orchestrator rewrite as long as the tool defines `run_check()` appropriately and outputs the uniform JSON payload.
- **Fail-Fast Loops**: If a tool scaling requires heavily blocked I/O logic (like hitting a slow docker container), the tool must internally implement timeouts wrapping the core execution to prevent stalling the parent loop.

## Future Stability Notes
Large-scale integration (50+ active tools) will inherently push the system from synchronous subprocess arrays toward parallelized, multi-threaded mapping using Python's `concurrent.futures`. However, this violates early-cycle determinism and must be tightly planned behind a rigid Blueprint before execution.
