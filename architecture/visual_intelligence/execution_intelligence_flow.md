---
title: Execution Intelligence Flow
description: Flow diagram mapping the sequential execution of the Verification Pipeline.
category: Visual Intelligence
version: 1.0.0
---

# Execution Intelligence Flow

This document maps the sequential execution of the active Intelligence Layer (Verification Pipeline). It details the flow from the user invoking the CLI down to the individual core tools, highlighting the single, deterministic path of execution to maintain **Invariant #9 (Linear Pipeline)**.

```mermaid
sequenceDiagram
    participant User
    participant CLI as cli/main.py
    participant Router as navigation/router.py
    participant Orch as navigation/orchestrator/verification_orchestrator.py
    participant CoreTools as tools/core/*.py
    participant Renderer as cli/display/verification_renderer.py

    User->>CLI: python cli/main.py verify
    activate CLI
    
    CLI->>Router: route_command('verify')
    activate Router
    
    Router->>Orch: run_verification()
    activate Orch
    
    Note over Orch,CoreTools: Sequential Tool Execution (Invariant #9)
    
    Orch->>CoreTools: Run local_dependency_check.py
    CoreTools-->>Orch: JSON Report (Status/Metrics)
    
    Orch->>CoreTools: Run workspace_hygiene_check.py
    CoreTools-->>Orch: JSON Report (Status/Metrics)
    
    Orch->>CoreTools: Run python_syntax_check.py
    CoreTools-->>Orch: JSON Report (Status/Metrics)
    
    Orch->>CoreTools: Run ant_boundary_enforcer.py
    CoreTools-->>Orch: JSON Report (Status/Metrics)
    
    Orch->>CoreTools: Run orphaned_tool_verifier.py
    CoreTools-->>Orch: JSON Report (Status/Metrics)
    
    Orch->>CoreTools: Run architecture_link_validator.py
    CoreTools-->>Orch: JSON Report (Status/Metrics)
    
    Orch->>CoreTools: Run filesystem_integrity_check.py
    CoreTools-->>Orch: JSON Report (Status/Metrics)

    Orch->>CoreTools: Run python_package_check.py
    CoreTools-->>Orch: JSON Report (Status/Metrics)

    Orch->>CoreTools: Run schema_validator_stub.py
    CoreTools-->>Orch: JSON Report (Status/Metrics)

    Orch->>CoreTools: Run registry_readiness_check.py
    CoreTools-->>Orch: JSON Report (Status/Metrics)
    
    Orch-->>Router: Aggregated Diagnostics Report
    deactivate Orch
    
    Router-->>CLI: Action Result
    deactivate Router
    
    CLI->>Renderer: render_verification_report(aggregated)
    activate Renderer
    Renderer-->>CLI: Formatted CLI Output
    deactivate Renderer
    
    CLI-->>User: Visual Output & Exit Code (0 or 1)
    deactivate CLI
```

## Architectural Notes
- The orchestrator maintains absolute control over the sequence. No tool is allowed to invoke another tool directly.
- The interface between `verification_orchestrator.py` and the core tools is strictly JSON over stdout.
- The `Renderer` layer never interacts directly with `tools/core/`. It only parses the aggregated dictionary strictly conforming to `verification_output_format.md`.
