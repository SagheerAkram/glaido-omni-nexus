# Tool Lifecycle Model

## Purpose
This specification details the lifecycle of an individual diagnostic or operational tool within the Glaido Omni-Nexus. It delineates the required phases an operational utility undergoes from initialization to successful termination and cleanup.

## Structural Overview
A tool's lifecycle is rigidly phase-locked to ensure no dangling processes or memory leaks happen:
1. **Initialization Phase**: Resolution of paths, parsing configuration (if any), and ensuring the required standard libraries are available.
2. **Execution Phase**: Running the core logic (e.g., traversing an AST, verifying an import). 
3. **Contract Emission Phase**: Consolidating findings into a Python dictionary.
4. **Serialization & Exit Phase**: Dumping the dictionary as JSON to `sys.stdout` and terminating with an explicit `sys.exit(0)` or `sys.exit(1)`.

## Interaction Model
- Tools expect no external network configuration. They operate solely on their explicit path or the implicit contextual path of the workspace root (`get_workspace_root()`).
- All errors are trapped via a definitive top-level `except Exception as e` guard block that securely reformats catastrophic logic failures into a sanitized JSON string. This guarantees that the Orchestrator rarely has to parse stack traces.

## Future Stability Notes
It is crucial that tools remain stateless across multiple runs. No tool should cache data on disk to speed up a subsequent run unless specifically requested and governed by an Architecture SOP. The zero-trust, stateless tool model ensures deterministic verification reporting.
