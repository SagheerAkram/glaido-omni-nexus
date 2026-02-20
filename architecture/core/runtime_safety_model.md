# Runtime Safety Model

## Purpose
This document codifies the core protections built into the Omni-Nexus runtime, establishing how the system guards against catastrophic cascades, hanging threads, and undefined behaviors during tool execution.

## Structural Overview
The safety model operates on the principle of isolation. Tool execution is fundamentally decoupled from the main orchestrator memory:
- **Subprocess Encapsulation**: Tools are launched as asynchronous `subprocess` calls. If a tool fails to terminate, it can be mathematically isolated and killed.
- **Non-Zero Exit Mapping**: A tool returning an exit code `>0` is interpreted uniformly as a localized failure, triggering the orchestrator to log a degraded state without breaking the primary event loop.
- **Synthesized Fallbacks**: Hard crashes trigger the `except Exception` outer loop in each tool to synthesize a standard JSON error, preventing the Orchestrator from ever receiving unparseable strings.

## Interaction Model
- **Orchestrator to CLI**: Safety checks are reported cleanly without halting execution unless the Orchestrator decides a cascaded failure guarantees total shutdown.
- **Tool to Host Engine**: No internal tool modifies `sys.path` dynamically or alters execution environments globally. Temporary files generated (e.g., lockfiles, logs) are rigidly flushed into `.tmp/` isolated spaces and wiped upon verification teardown.

## Future Stability Notes
Any expansion introducing complex resource binding (e.g., parallel agents querying databases) must emulate this model by separating execution threads and enforcing rigid, short-lived timeout limits. Long-running tasks must periodically yield standardized heartbeat JSON packets.
