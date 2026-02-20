# Dormant State Model

## Purpose
Provides a conceptual map distinguishing between what actions the Omni-Nexus can and cannot perform while in its baseline locked condition.

## Structural Overview
Dormancy is the default mode of operation. It is inherently read-only and diagnostic, ensuring the environment remains static when developers are inspecting health or mapping topologies.

## Interaction Model
```text
┌───────────────────────────────┐
│     DORMANT STATE (LOCKED)    │
│                               │
│  [✓] Verification Scripts     │
│  [✓] Discovery Audits         │
│  [✓] Markdown Normalization   │
│  [✓] Map Link Generations     │
│                               │
│  [✗] Execute Subprocesses     │
│  [✗] Modify Core Python       │
│  [✗] Generate Executables     │
│  [✗] Change External State    │
└───────────────┬───────────────┘
                │
         (Manual Bypass)
                │
                ▼
┌───────────────────────────────┐
│        EXPANSION STATE        │
│  [✓] Feature Prototyping      │
│  [✓] Dynamic Tool Gen         │
└───────────────────────────────┘
```

## Future Stability Notes
The Dormant State ensures that any multi-agent operation running continuously acts identically to a purely read-only observer. Maintaining this read/write partition minimizes drift on the `master` branch.
