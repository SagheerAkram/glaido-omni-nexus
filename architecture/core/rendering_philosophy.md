# Rendering Philosophy

## Purpose
This document codifies the core visual and user-experience principles dictating how the system communicates state. It ensures the Omni-Nexus aesthetics feel unified, clear, and uncompromisingly premium without requiring heavy third-party UI libraries like `rich` or `colorama`.

## Structural Overview
Rendering logic sits apart from operational logic. The `cli/display/formatter.py` acts as the definitive design system:
- **Typographic Constants**: Enforces specific ANSI codes (`LIME_GREEN`, `CYAN`, `DIM`, `BOLD`).
- **Geometric Elements**: Employs premium Unicode character sets for table composition, vertical alignment, and hierarchical dividers.
- **Fail-Safe Toggles**: Dynamically supports stripping all ANSI and complex Unicode logic if `COLOR_ENABLED` is switched to False or if terminal emulation fails.

## Interaction Model
- Scripts needing to output data never print raw stylized strings independently. They invoke the `.formatter` and `.verification_renderer` functions.
- The `formatter.py` acts purely functionally: `string in -> formatted string out`. 
- Structural functions like `create_table()` or `progress_bar()` enforce padding and alignment, dynamically shifting based on data width.

## Future Stability Notes
As new expansion modules are integrated, developers must lean entirely on existing format utilities. The usage of hardcoded ANSI escapes outside of `formatter.py` is strictly prohibited. Future iterations may add custom spinners or async loading bars, provided they degrade gracefully under non-interactive execution constraints.
