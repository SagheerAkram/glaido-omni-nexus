# Tool Execution Chain

## Purpose
This document maps the lifecycle of a single tool execution process inside the Omni-Nexus. Tools intentionally behave as isolated subprocesses to protect horizontal stability and contain catastrophic faults.

## Structural Overview
A tool transitions through an initial safety wrapper into a main logic execution block, terminating by outputting a JSON payload directly to the standard output buffer. 

## Interaction Model
```text
       [ ORCHESTRATOR CALL ]
                 │
                 ▼
       ( subprocess.run() )
                 │
┌────────────────┴────────────────┐
│         TOOL ENVELOPE           │
│                                 │
│  1. Check `__main__` entry      │
│  2. `try:`                      │
│      a) Run `run_check()`       │
│      b) Resolve target paths    │
│      c) Compute health          │
│      d) Build `report` dict     │
│  3. `except Exception as e:`    │
│      a) Catch catastrophic drop │
│      b) Build `fallback` dict   │
│                                 │
│  4. `print(json.dumps(...))`    │
│  5. `sys.exit(0` or `1)`        │
└────────────────┬────────────────┘
                 │
                 ▼
        [ ORCHESTRATOR PARSES JSON ]
```

## Future Stability Notes
By forcing every tool to manually serialize and print JSON instead of returning Python objects, we maintain process isolation. Future architectural extensions can easily adapt tooling in other languages (e.g., Rust binaries) with zero friction as long as they follow the identical JSON stdout emission contract.
