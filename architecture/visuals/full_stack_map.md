# Full Stack Map

## Purpose
This document provides a top-down, high-level map of the entire Glaido Omni-Nexus stack. It visualizes the hierarchical relationship between the core pillars: Architecture, Navigation, Tools, and the terminal entry points.

## Structural Overview
The Omni-Nexus is divided into explicit layers, each isolated to prevent scope bleed.
- **Top Layer**: CLI / UI
- **Middle Layer**: Navigation / Orchestration
- **Bottom Layer**: Architecture / Tools / Agents

## Interaction Model
```text
[ USER INTERACTION ]
        │
        ▼
┌─────────────────────────────────┐
│        cli/main.py (ENTRY)      │
│  (Delegates Commands to Router) │
└─────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────┐
│       navigation/router/        │
│       Command Dispatcher        │
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│   navigation/orchestrator/      │
│  (e.g., verification_orchestrator)│
└─┬─────────────────────────────┬─┘
  │ READS RULES                 │ EXECUTES
  ▼                             ▼
┌──────────────────┐    ┌──────────────────┐
│ architecture/    │    │ tools/core/      │
│ (A.N.T., B.L.A.S.T)│    │ (Validators,     │
│ SPECIFICATIONS   │    │ Diagnostics)     │
└──────────────────┘    └──────────────────┘
```

## Future Stability Notes
The stack map is immutable for the foreseeable future. Any attempt to bypass the `navigation` layer (e.g., `cli` directly executing a `tool`) violates the stack hierarchy and will risk pipeline degradation.
