# Static Analysis Patterns

## Purpose
Establishes the standard conventions for static code analysis within the Omni-Nexus, ensuring tools remain completely read-only, robust against ill-formed code, and entirely isolated from runtime side-effects.

## Structural Overview
Static analysis is the backbone of the system's "Offline-First" capability. It relies on standard library text traversal rather than runtime inspection (e.g., `importlib` for everything). 

## Interaction Model
- **Tokenization Over Import**: If a tool must verify the components of a file, we strongly prefer static parsing (such as standard library `ast` parsing) rather than dynamically importing it. Dynamic imports introduce potential initialization bugs and side-effects.
- **Fail-Safe Parsing**: Since we often scan files generated actively by models or currently being edited by developers, the static analysis parser must defensively handle malformed files (e.g., catching `SyntaxError` and gracefully logging it) rather than blowing up the entire Orchestrator process.

## Future Stability Notes
Relying strictly on static analysis enforces extreme safety. Before we ever introduce dynamic runtime testing arrays (where arbitrary Python files are executed), the static analysis tools must achieve near 100% confidence. Future expansion into Java or C++ tools will mirror these exact regular expression or static-graph analysis patterns.
