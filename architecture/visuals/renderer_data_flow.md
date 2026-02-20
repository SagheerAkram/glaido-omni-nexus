# Renderer Data Flow

## Purpose
Displays how raw JSON generated from tools translates into styled, colored terminal visual layers, isolating operational parsing from rendering aesthetics.

## Structural Overview
Display components exist in a clean hierarchy. The specific rendering of a complex data type (like a verification report) utilizes primitive layout functions from a core formatter module.

## Interaction Model
```text
[ RAW JSON LIST ]
      │
      ▼
[ VERIFICATION_RENDERER.PY ]
      │
      ├──> Analyzes Status Array (`ready`, `degraded`, `error`)
      │
      ├──> Calls `formatter.create_table(headers, rows)`
      │      │
      │      ├──> `formatter.kv_pair()`
      │      ├──> `formatter.lime() / formatter.red()`
      │      └──> Calculates Unicode padding geometries (`┌`, `┬`, `┐`)
      │
      └──> Returns massive formatted string `\n` block
      │
      ▼
[ sys.stdout.write ] -> Rendered to Terminal
```

## Future Stability Notes
This exact flow allows us to swap a terminal emulator rendering engine for web-rendering engines extremely easily, or toggle between color/monochrome without altering anything further upstream. The format utilities are primitive constants that must not be altered drastically.
