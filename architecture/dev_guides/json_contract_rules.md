# JSON Contract Rules

## Purpose
Governs the strict communication boundary format utilized to shuttle diagnostic health states back and forth between disparate layers of the Omni-Nexus stack.

## Structural Overview
Every diagnostic tool acts an independent binary process emitting exactly one stdout payload formatted strictly as JSON. Any deviations, trailing characters, or unstructured text dumps break the contract and will deliberately fail the Orchestrator loop.

## Interaction Model
The contract guarantees:
1. `"category"`: String literal identifying the check type.
2. `"status"`: Must heavily conform to enum values `["ready", "degraded", "error", "healthy"]`.
3. `"timestamp"`: Standardized UTC ISO format string.
4. `"results"`: Dictionary mapping specifics.
5. `"message"`: Concise human string for direct terminal echoing.
6. `"actionable"`: Boolean triggering the rendering of remediation tips.
7. `"remediation"`: Nullable string describing the immediate fix path for simple errors.

## Future Stability Notes
This exact contract effectively acts as the "API" of the system, completely negating the need for complex internal state sharing or Python function-call coupling. Future additions to the JSON spec must be extremely carefully negotiated via an approved SOP blueprint, as breaking changes will immediately crash the CLI Renderer.
