---
title: Layer Enforcement Diagram
description: Visualization of the A.N.T. architecture separation mapping specifically how it is policed.
category: Visual Intelligence
version: 1.0.0
---

# Layer Enforcement Diagram

This map details how **Invariant #2 (A.N.T Separation)** is structurally enforced via automated runtime checks, specifically the newly introduced `ant_boundary_enforcer.py`.

```mermaid
graph LR
    classDef toolsLayer fill:#bbdefb,stroke:#1565c0,stroke-width:2px;
    classDef navLayer fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px;
    classDef archLayer fill:#ffe0b2,stroke:#ef6c00,stroke-width:2px;
    classDef cliLayer fill:#d1c4e9,stroke:#4527a0,stroke-width:2px;
    classDef enforcer fill:#ffcdd2,stroke:#c62828,stroke-width:3px;

    tools[tools/ (Cognition & Work)]:::toolsLayer
    nav[navigation/ (Routing & Pipeline)]:::navLayer
    arch[architecture/ (Law & State)]:::archLayer
    cli[cli/ (I/O & Display)]:::cliLayer

    enforcer((ant_boundary_enforcer.py)):::enforcer

    cli -->|Valid| nav
    nav -->|Valid| tools
    tools -.->|Reads| arch
    nav -.->|Reads| arch

    tools -.->|"FORBIDDEN!"| cli
    nav -.->|"FORBIDDEN!"| cliLayer

    enforcer -.->|Regex / AST Scan| tools
    enforcer -.->|Regex / AST Scan| nav
```

## Enforcement Rules Explored

1. `tools/` **must never** import from `cli/`
   - Tools are context-agnostic scripts. They return structured data (JSON), never formatting text with ANSI codes. Coupling tools to the CLI layer prevents them from being operated correctly by agents.
2. `navigation/` **must never** import from `cli/display/`
   - Routers orchestrate sequence. Renderers parse output. If the navigator handles its own rendering, the CLI is bypassed, fracturing the rendering consistency requirement.

The `ant_boundary_enforcer.py` script utilizes the Python `ast` module to read all scripts inside `tools/` and `navigation/` comparing node imports against the blacklist. This guarantees that technical debt or quick hacks do not erode the A.N.T configuration over time.
