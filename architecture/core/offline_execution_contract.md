# Offline Execution Contract

## Purpose
This document formally defines the Offline-First invariant embedded within the Glaido Omni-Nexus. It ensures that the system's core capabilities, particularly validation and architectural diagnostics, remain fully functional without external network dependencies.

## Structural Overview
The offline execution contract mandates that:
- **No Third-Party APIs**: Core tools cannot reach out to external services (e.g., package managers, linters hosted remotely) for their validation logic.
- **Local AST/Standard Library Reliance**: All static analysis must leverage standard library modules (e.g., `ast`, `json`, `pathlib`) available directly in the host's Python environment.
- **Standalone Integrity**: The system must be capable of rebuilding its own understanding of its state from disk, without pulling state from cloud providers or databases.

## Interaction Model
- When an Orchestrator runs, it inherently assumes standard library availability. The `local_dependency_check.py` tool verifies this explicit contract on every run.
- Network calls are strictly isolated to completely separate, clearly demarcated agent layers (if they exist in the future), but never in the core verification loop or structural diagnostic tools.

## Future Stability Notes
As new expansion modules are Blueprint-linked into the system, they undergo the B.L.A.S.T. lifecycle. A module that attempts a network request during standard verification will instantly violate this contract. If network-required diagnostic tools are ever proposed, they must be explicitly designated and gated behind a separate `--online` operational flag.
