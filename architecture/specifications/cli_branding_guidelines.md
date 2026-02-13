# CLI Branding Guidelines — Specification

> **Purpose**: Define visual identity and presentation standards for CLI interface  
> **Phase**: Stylize (Phase 4)  
> **Status**: Documentation Only — No Executable Logic

---

## Core Brand Identity

**System Persona**: Enterprise-grade, deterministic, cyberpunk-aesthetic AI ecosystem

**Visual Tone**:
- Professional and authoritative
- Minimalist and high-contrast
- Cyberpunk-inspired terminal aesthetic
- Deterministic and predictable output
- No playful or casual language

---

## Brand Color Palette

### Primary Colors

| Color Name | Hex Code | RGB Values | Usage |
|------------|----------|------------|-------|
| **Lime Green** | `#BFF549` | `191, 245, 73` | Primary accent, success states, highlights |
| **White** | `#FFFFFF` | `255, 255, 255` | Primary text, content display |
| **Black** | `#000000` | `0, 0, 0` | Background (terminal default) |

### ANSI Escape Codes

**Lime Green**: `\033[38;2;191;245;73m`  
**White**: `\033[38;2;255;255;255m`  
**Black**: `\033[38;2;0;0;0m` (rarely needed, terminal default)  
**Reset**: `\033[0m`

---

## Color Usage Rules

### Lime Green Usage

**Approved Contexts**:
- System name in banners ("GLAIDO OMNI-NEXUS")
- Success indicators (✅, "READY", "SUCCESS")
- Primary action verbs (CREATE, VERIFY, EXECUTE)
- Section headers in output
- Critical system identifiers (agent names, tool names)

**Prohibited Contexts**:
- Error messages
- Warning text
- Body content (use white instead)
- Log timestamps

---

### White Usage

**Approved Contexts**:
- All body text and content
- Data display (JSON output, tables, lists)
- Secondary labels
- Informational messages
- Log entries
- Documentation snippets

**Prohibited Contexts**:
- Do not override with other colors unless semantically required (errors, warnings)

---

### Semantic Color Extensions

While lime green, white, and black are the core brand colors, additional semantic colors may be used for specific UI states:

| State | Color | ANSI Code | Usage |
|-------|-------|-----------|-------|
| **Error** | Red | `\033[91m` | Error messages, failure indicators |
| **Warning** | Yellow | `\033[93m` | Warning messages, degraded states |
| **Info** | Cyan | `\033[96m` | Optional info highlights |

**Note**: Semantic colors are supplementary only. Lime green remains the primary brand accent.

---

## ASCII Banner Behavior

### Startup Banner

**Trigger**: Application entry point (future `glaido` CLI invocation)

**Content**:
```
╔════════════════════════════════════════════════════════════╗
║                  GLAIDO OMNI-NEXUS                         ║
║              Offline AI Agent Ecosystem                    ║
╚════════════════════════════════════════════════════════════╝
```

**Formatting Rules**:
- "GLAIDO OMNI-NEXUS" in **lime green**
- Subtitle "Offline AI Agent Ecosystem" in **white**
- Box-drawing characters in **white**
- Single blank line before and after banner
- Banner appears once per session

---

### Command Headers

**Trigger**: Start of command execution output

**Format**:
```
╔══════════════════════════════════════╗
║  [COMMAND NAME]                       ║
╚══════════════════════════════════════╝
```

**Rules**:
- Command name in **lime green** and uppercase
- Box-drawing characters in **white**
- No subtitle line
- Compact spacing (no extra blank lines)

**Example**:
```
╔══════════════════════════════════════╗
║  VERIFY                               ║
╚══════════════════════════════════════╝
```

---

### Section Dividers

**Trigger**: Separating output sections within a command

**Format**:
```
─────────────────────────────────────────
[Section Name]
─────────────────────────────────────────
```

**Rules**:
- Section name in **lime green**
- Divider lines in **white**
- Single blank line before divider
- No blank line after divider

---

## Logging Tone and Content

### Tone Characteristics

**Required Attributes**:
- Professional and technical
- Concise and information-dense
- Deterministic (no randomized messages)
- Actionable (provide context for errors)
- Enterprise-appropriate (no slang, emoji, or casual language)

**Prohibited Attributes**:
- Playful or humorous tone
- Anthropomorphization of system components
- Excessive verbosity
- Vague or ambiguous language

---

### Log Message Structure

**Standard Format**:
```
[TIMESTAMP] [LEVEL] [COMPONENT] Message content
```

**Field Definitions**:
- `TIMESTAMP`: ISO8601 local time (e.g., `2026-02-13T21:39:00+05:00`)
- `LEVEL`: `INFO`, `WARN`, `ERROR`, `DEBUG`
- `COMPONENT`: Tool/agent/module identifier (e.g., `orchestrator`, `local_dependency_check`)
- `Message`: Concise description of event

**Color Coding**:
- Timestamp: **white**
- Level: Semantic color (INFO=white, WARN=yellow, ERROR=red, DEBUG=cyan)
- Component: **lime green**
- Message: **white**

---

### Log Level Guidelines

#### INFO

**Usage**: Routine operational events

**Examples**:
- "Verification started"
- "Agent registry loaded"
- "Tool execution completed"

**Tone**: Neutral, factual

---

#### WARN

**Usage**: Non-critical issues or degraded states

**Examples**:
- "Temp directory writable but low disk space"
- "Agent count is zero (no agents registered)"
- "Backup file older than 7 days"

**Tone**: Cautionary but not alarming

---

#### ERROR

**Usage**: Critical failures requiring attention

**Examples**:
- "Python version 3.7 does not meet requirement (≥3.8)"
- "Registry file not found: agents/_registry.json"
- "Tool execution timeout after 30 seconds"

**Tone**: Direct, actionable, include error context

---

#### DEBUG

**Usage**: Detailed diagnostic information (future dev mode)

**Examples**:
- "Parsed JSON payload: {...}"
- "Subprocess invoked: ['python', 'tools/core/...']"
- "Schema validation passed: agent_config"

**Tone**: Technical, verbose

---

## Output Formatting Standards

### Tables

**Format**: Unicode box-drawing characters

**Header Row**: **Lime green** text, white separators

**Data Rows**: **White** text

**Example**:
```
┌──────────────────┬──────────┬────────────┐
│ Component        │ Status   │ Details    │
├──────────────────┼──────────┼────────────┤
│ Local Deps       │ ✅ READY │ Python 3.11│
│ Filesystem       │ ✅ HEALTHY│ All OK    │
│ Schema Validator │ ✅ READY │ Importable│
│ Agent Registry   │ ✅ READY │ 0 agents  │
└──────────────────┴──────────┴────────────┘
```

**Alignment**: Left-aligned text, consistent column widths

---

### Lists

**Bullet Lists**: Use `•` character (not `-` or `*`)

**Nested Lists**: Indent with 2 spaces per level

**Color Rules**:
- List labels: **Lime green**
- List items: **White**

**Example**:
```
Verification Results:
  • Local Dependencies: ✅ READY
  • Filesystem Integrity: ✅ HEALTHY
  • Schema Validation: ✅ READY
  • Agent Registry: ✅ READY
```

---

### Status Indicators

**Success**: `✅` followed by uppercase status text in **lime green**

**Warning**: `⚠️` followed by uppercase status text in **yellow**

**Error**: `❌` followed by uppercase status text in **red**

**Info**: `ℹ️` followed by text in **white**

**Examples**:
- `✅ READY`
- `⚠️ DEGRADED`
- `❌ ERROR`
- `ℹ️ System operational`

---

### JSON Output Display

**Raw JSON**: Use **white** for entire JSON payload

**Syntax Highlighting** (future enhancement):
- Keys: **lime green**
- String values: **white**
- Numeric values: **cyan**
- Booleans: **yellow**
- Null: **red**

**Indentation**: 2-space indent for readability

**Example** (basic white formatting for now):
```json
{
  "orchestrator": "verification_orchestrator",
  "overall_status": "ready",
  "verifications": {
    "local_dependencies": {
      "status": "ready"
    }
  }
}
```

---

## Command Completion Messages

### Success Completion

**Format**:
```
╔════════════════════════════════════╗
║  ✅ [COMMAND] COMPLETE             ║
╚════════════════════════════════════╝
```

**Command name**: **Lime green**  
**"COMPLETE"**: **Lime green**

---

### Error Completion

**Format**:
```
╔════════════════════════════════════╗
║  ❌ [COMMAND] FAILED               ║
╚════════════════════════════════════╝

Error: [error message]
```

**Command name**: **Red**  
**"FAILED"**: **Red**  
**Error message**: **White**

---

## Progressive Disclosure

### Verbosity Levels

**Default (Standard)**:
- Show high-level status only
- Display summary results
- Hide detailed diagnostics

**Verbose Mode** (future `--verbose` flag):
- Show all log levels (including DEBUG)
- Display full JSON payloads
- Include timing information

**Quiet Mode** (future `--quiet` flag):
- Show errors only
- Suppress INFO and DEBUG
- Minimal output

---

## Loading and Progress Indicators

### Static Indicators

**Preferred**: Use deterministic status messages, not spinners

**Format**:
```
[COMPONENT] Running...
[COMPONENT] Complete ✅
```

---

### Future Enhancement: Progress Bars

**Format** (not yet implemented):
```
Verification Progress: [████████░░] 80% (4/5 tools complete)
```

**Rules**:
- Use box-drawing characters for bar
- Show percentage and absolute progress
- Completed portion: **Lime green**
- Remaining portion: **White** (dim)

---

## Error Message Guidelines

### Structure

**Format**:
```
❌ ERROR: [Error Type]

[Detailed error description]

Context:
  • Field: Value
  • Field: Value

Suggested Action:
  [Specific remediation steps]
```

**Color Rules**:
- Error icon and "ERROR": **Red**
- Error type: **Red**
- Description: **White**
- Context labels: **Lime green**
- Context values: **White**
- Suggested action: **White**

---

### Error Categories

**System Error**: Infrastructure or environment issues

**Validation Error**: Input/schema validation failures

**Execution Error**: Tool or agent execution failures

**User Error**: Invalid command usage or missing arguments

---

## Consistency Requirements

### Cross-Command Consistency

All commands must:
- Use identical banner formatting
- Apply same color rules
- Follow same log message structure
- Use same status indicators
- Maintain same tone

### Version Consistency

CLI appearance must remain stable across versions unless explicitly updated in this specification.

---

## Accessibility Considerations

### ANSI Compatibility

All formatting must gracefully degrade on terminals without 24-bit color support:
- RGB colors fall back to nearest 256-color equivalent
- If ANSI not supported, emit plain text
- Core information remains readable without colors

### Screen Reader Compatibility

Status indicators must include text equivalents:
- "SUCCESS" not just ✅
- "ERROR" not just ❌
- "WARNING" not just ⚠️

---

## Implementation Notes

### Future CLI Module Structure

**Formatter Module** (future: `cli/display/formatter.py`):
- Color constant definitions
- ANSI code utilities
- Text formatting functions

**Banner Module** (future: `cli/display/banner.py`):
- ASCII art generation
- Header formatting
- Section dividers

**Logger Module** (future: `cli/display/logger.py`):
- Structured logging
- Level-based formatting
- Color application

**Note**: No implementation yet — specifications only during Stylize phase

---

## Summary

CLI branding ensures:
- **Consistency**: Unified visual identity across all commands
- **Professionalism**: Enterprise-appropriate tone and aesthetics
- **Accessibility**: Graceful degradation and screen reader compatibility
- **Brand Alignment**: Lime green accent maintains Glaido identity
- **Clarity**: High-contrast, readable output for terminal environments

---

**Last Updated**: 2026-02-13T21:40:00+05:00  
**Status**: Stylize specification — awaiting implementation in future phases
