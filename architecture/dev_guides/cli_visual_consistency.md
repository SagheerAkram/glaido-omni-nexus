# CLI Visual Consistency

## Purpose
Establishes the absolute styling requirements for the terminal interface, ensuring the Glaido Omni-Nexus feels premium, uniform, and instantly recognizable across all text outputs.

## Structural Overview
The CLI acts as the unified 'face' of the system. The `cli/display/formatter.py` and `cli/display/verification_renderer.py` dictate formatting to avoid fractured UX.

## Interaction Model
- **Color Palette Limits**: Developers must strictly adopt standard ANSI combinations (`bold_lime`, `dim_white`, `bright_red`). Direct ANSI injections (`\033[...`) outside of the `formatter.py` constants are totally forbidden to prevent cross-OS graphical tearing.
- **Table Spacing Rules**: 
  - All status tables must implement a left-aligned, uniform 2-space padding block. 
  - Keys (i.e. 'Component:') must be aligned across rows. 
  - Dynamic content (`values`) must truncate elegantly rather than blowing out terminal wrap widths.
- **Unicode Line Drafting**: Boxes and separators must utilize `┌`, `─`, `┬`, `┐` character sets. `+---+` ASCII fallbacks are only allowed if the terminal strictly reports zero Unicode support.

## Future Stability Notes
Scaling the CLI visual consistency as tools grow in number dictates moving toward an interactive standard (like the `rich` Python library) instead of handmade ANSI codes. Any such transition must involve a full rewrite of the `formatter.py` and remain backwards compatible with existing Orchestrator outputs.
