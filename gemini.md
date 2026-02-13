# 🧠 GEMINI.MD — PROJECT CONSTITUTION

> **Status**: Glaido Omni-Nexus System Charter  
> **Version**: 1.0.0  
> **Architecture**: A.N.T. (Architecture → Navigation → Tools)  
> **Protocol**: B.L.A.S.T. (Blueprint → Link → Architect → Stylize → Trigger)

---

## 📜 SYSTEM IDENTITY

Glaido Omni-Nexus is a **massive, headless AI ecosystem** for protocol-driven autonomous agent orchestration.

### Core Principles
1. **Data-First Methodology**: Never guess schemas; define before implementation
2. **Modular Expansion**: Each new agent/feature expands the ecosystem organically
3. **Deterministic Execution**: All logic in tools/, never in LLM reasoning
4. **Self-Annealing**: System repairs itself and updates SOPs after failures
5. **CLI-Only Interface**: No web UI, no HTML, no CSS

---

## 🏛️ ARCHITECTURAL INVARIANTS

### A.N.T. Layer Separation (IMMUTABLE)

```
┌─────────────────────────────────────┐
│   LAYER 1: ARCHITECTURE/            │
│   - Markdown SOPs & Documentation   │
│   - Technical Specifications        │
│   - Behavioral Rules                │
│   - Edge Case Handling              │
└─────────────────────────────────────┘
             ↓ (reads)
┌─────────────────────────────────────┐
│   LAYER 2: NAVIGATION/              │
│   - Decision Routing Logic          │
│   - Task Orchestration              │
│   - Agent Coordination              │
│   - Data Flow Management            │
│   ❌ NO HEAVY LOGIC HERE            │
└─────────────────────────────────────┘
             ↓ (calls)
┌─────────────────────────────────────┐
│   LAYER 3: TOOLS/                   │
│   - Deterministic Python Scripts    │
│   - Atomic Execution Units          │
│   - Testable & Modular              │
│   - All Business Logic              │
└─────────────────────────────────────┘
```

### Forbidden Actions
- ❌ Writing tools before architecture exists
- ❌ Implementing logic in navigation layer
- ❌ Guessing data schemas
- ❌ Creating monolithic files
- ❌ Generating web interfaces

### PROTOCOL 0 ENFORCEMENT (Critical)
> **Updated**: 2026-02-13T20:55:05+05:00  
> **Decision**: Option C (Hybrid Cleanup) — Architecturally Corrected

**IMMUTABLE RULE**: Navigation and Tools layers remain **EMPTY of executable logic** until:
1. ✅ Discovery Questions answered
2. ✅ Blueprint Phase SOPs generated in `architecture/`
3. ✅ User approves architectural plan

**Folder Structure Philosophy**:
- Massive directory tree = **visual scaffolding for future expansion**
- Folders exist to show **scale and intent**, not current implementation
- All execution frozen until architecture is proven sound

**What IS allowed in Protocol 0**:
- ✅ Folder structure (intentional massive scale)
- ✅ Markdown documentation
- ✅ JSON schemas and configurations
- ✅ Root memory files

**What is FORBIDDEN until Blueprint SOPs exist**:
- ❌ Python scripts (`.py` files) in `navigation/` or `tools/`
- ❌ Functional logic of any kind
- ❌ Tool implementations
- ❌ Navigation code
- ❌ Agent behavior scripts

**Hybrid Cleanup Confirmation**:
> Navigation and Tools layers remain **structurally present but executionally empty** until Discovery Questions are resolved and SOPs exist. This prevents premature execution while maintaining architectural scale.

---

## 📊 JSON DATA SCHEMAS

### Agent Configuration Schema
```json
{
  "agent_config": {
    "type": "object",
    "required": ["agent_id", "name", "type", "capabilities"],
    "properties": {
      "agent_id": {
        "type": "string",
        "pattern": "^agent_[a-z0-9_]+$",
        "description": "Unique agent identifier"
      },
      "name": {
        "type": "string",
        "description": "Human-readable agent name"
      },
      "type": {
        "type": "string",
        "enum": ["discovery", "execution", "monitoring", "custom"],
        "description": "Agent classification"
      },
      "capabilities": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "List of agent capabilities"
      },
      "dependencies": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "Required tool dependencies"
      },
      "created_at": {
        "type": "string",
        "format": "date-time"
      }
    }
  }
}
```

### Tool Execution Payload Schema
```json
{
  "tool_execution": {
    "type": "object",
    "required": ["tool_id", "input_data", "execution_context"],
    "properties": {
      "tool_id": {
        "type": "string",
        "pattern": "^tool_[a-z0-9_]+$"
      },
      "input_data": {
        "type": "object",
        "description": "Tool-specific input parameters"
      },
      "execution_context": {
        "type": "object",
        "properties": {
          "session_id": {"type": "string"},
          "agent_id": {"type": "string"},
          "timestamp": {"type": "string", "format": "date-time"},
          "priority": {"type": "integer", "minimum": 0, "maximum": 10}
        }
      },
      "output_destination": {
        "type": "string",
        "description": "Where to send results"
      }
    }
  }
}
```

### Navigation Routing Schema
```json
{
  "routing_decision": {
    "type": "object",
    "required": ["task_id", "route_type", "target"],
    "properties": {
      "task_id": {
        "type": "string"
      },
      "route_type": {
        "type": "string",
        "enum": ["agent_spawn", "tool_call", "workflow_trigger", "error_recovery"]
      },
      "target": {
        "type": "string",
        "description": "Agent ID or Tool ID to route to"
      },
      "payload": {
        "type": "object",
        "description": "Data to pass to target"
      },
      "fallback": {
        "type": "string",
        "description": "Fallback route if target fails"
      }
    }
  }
}
```

### System Event Log Schema
```json
{
  "system_event": {
    "type": "object",
    "required": ["event_id", "event_type", "timestamp", "severity"],
    "properties": {
      "event_id": {
        "type": "string",
        "format": "uuid"
      },
      "event_type": {
        "type": "string",
        "enum": ["info", "warning", "error", "critical", "success"]
      },
      "timestamp": {
        "type": "string",
        "format": "date-time"
      },
      "severity": {
        "type": "integer",
        "minimum": 0,
        "maximum": 5
      },
      "source": {
        "type": "string",
        "description": "Agent, Tool, or System component that generated event"
      },
      "message": {
        "type": "string"
      },
      "metadata": {
        "type": "object",
        "description": "Additional context"
      }
    }
  }
}
```

---

## 🎨 BRAND IDENTITY

### Color Palette (RGB Values)
```json
{
  "brand_colors": {
    "lime_green": {
      "hex": "#BFF549",
      "rgb": [191, 245, 73],
      "ansi_code": "\u001b[38;2;191;245;73m"
    },
    "white": {
      "hex": "#FFFFFF",
      "rgb": [255, 255, 255],
      "ansi_code": "\u001b[38;2;255;255;255m"
    },
    "black": {
      "hex": "#000000",
      "rgb": [0, 0, 0],
      "ansi_code": "\u001b[38;2;0;0;0m"
    }
  }
}
```

### ASCII Logo Template
```
Placeholder for rounded "G" chat-bubble emblem
(To be designed in Phase 4 - Stylize)
```

---

## 🔄 B.L.A.S.T. PROTOCOL ENFORCEMENT

### Phase Gate Requirements
| Phase | Entry Criteria | Exit Criteria |
|-------|---------------|---------------|
| **Blueprint (B)** | Discovery Questions answered | Architecture SOPs documented |
| **Link (L)** | SOPs complete | Connection checks simulated |
| **Architect (A)** | Connection verified | All tools + navigation built |
| **Stylize (S)** | Tools functional | CLI branding complete |
| **Trigger (T)** | System tested | Automation deployed |

### Self-Annealing Repair Loop
```
1. Detect tool failure
2. Capture error context
3. Patch script deterministically
4. Retest until success
5. Update architecture/ SOP
6. Commit changes to prevent recurrence
```

---

## 🛠️ BEHAVIORAL RULES

### Error Handling
- All errors must be caught and logged
- No silent failures
- Navigation layer routes to repair tools on failure
- SOPs updated after every unique failure

### Agent Spawning
- Agents must register in `agents/_registry.json`
- Each agent gets dedicated folder with config.json, manifest.md, behavior.py
- Agents never share state directly; use navigation layer

### Tool Development
- Tools must be atomic (single responsibility)
- All tools must have test coverage
- No external API calls without architecture/ specification
- Tools return structured JSON, never print to stdout

---

## 🔐 SYSTEM CONSTRAINTS

### Immutable Rules (DO NOT VIOLATE)
1. No web interfaces (CLI only)
2. No schema guessing (document first)
3. No logic in navigation layer
4. No tools before architecture
5. All agents self-contained in agents/

---

## 📋 DISCOVERY QUESTIONS (ANSWERED — 2026-02-13T20:58:39+05:00)

### 1. North Star
**Q**: What is the singular desired outcome of Omni-Nexus?  
**A**: Build a modular offline AI infrastructure that autonomously generates, manages, and repairs its own CLI agents and workflows using protocol-driven architecture.

### 2. Integrations
**Q**: Which external services or APIs are expected?  
**A**: None initially — fully local/offline-first design. Future-ready architecture for optional GitHub API and local LLM connectors, but keep disabled for now.

### 3. Source of Truth
**Q**: Where does primary data live?  
**A**: Local filesystem + structured JSON schemas defined in `gemini.md`, with runtime data stored inside `.tmp/` and agent-specific folders.

### 4. Delivery Payload
**Q**: Where should final outputs go?  
**A**: Primary output through structured CLI stdout plus generated agent folders/modules written directly into the project workspace.

### 5. Behavioral Rules
**Q**: Tone, restrictions, or system personality constraints?  
**A**: Professional, deterministic, cyberpunk enterprise tone; lime-green branded CLI output; verbose logging enabled; never delete or overwrite user data without explicit confirmation.

---

**Version**: 1.0.0  
**Last Updated**: 2026-02-13T20:43:52+05:00  
**Status**: Constitution initialized — awaiting Blueprint Phase discoveries
