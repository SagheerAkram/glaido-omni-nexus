# A.N.T. Layer Boundaries

## Purpose
Visually demarcates the hard logical boundaries isolating Architecture, Navigation, and Tools from each other to prevent structural bleed.

## Structural Overview
Dependencies map downwards. Bottom layers have zero awareness of the layers above them.

## Interaction Model
```text
[ NAVIGATION ] (Aware of Tools & Architecture)
      │                    │
      ▼                    ▼
[ ARCHITECTURE ]  <--->  [ TOOLS ] (Unaware of Architecture & Navigation)
(Strict Static Data)     (Strict Runtime Code)
      │
      ├──> Rules, Schemas
```
*Correction*: The Architecture layer does not directly interact with Tools. It defines the rules that Navigation uses to orchestrate Tools.

```text
       ┌───────────────┐
       │  NAVIGATION   │ (Conductor)
       └──────┬────────┘
              │ (reads specs, runs executables)
       ┌──────┴────────┐
       ▼               ▼
┌────────────┐   ┌────────────┐
│ ARCHITECTURE│   │   TOOLS    │
│ (Source of  │   │ (Stateless │
│   Truth)    │   │  Workers)  │
└────────────┘   └────────────┘
```

## Future Stability Notes
Enforcing this exact boundary ensures that if a specific Tool module becomes deprecated or breaks, it never contaminates the Architecture specs or disrupts the core Routing logic in the Navigation space. Tools are disposable; Navigation is resilient; Architecture is immortal.
