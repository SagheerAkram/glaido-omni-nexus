# CLI Specifications — Brand Identity & Interface Design

> **Purpose**: Define CLI interface, ANSI color system, and cyberpunk branding  
> **Layer**: Architecture (Specification)  
> **Updated**: 2026-02-13T20:58:39+05:00

---

## 🎨 BRAND IDENTITY

### Color Palette
| Color | Hex | RGB | ANSI Escape Code |
|-------|-----|-----|------------------|
| **Lime Green** | `#BFF549` | `191, 245, 73` | `\033[38;2;191;245;73m` |
| **White** | `#FFFFFF` | `255, 255, 255` | `\033[38;2;255;255;255m` |
| **Black** | `#000000` | `0, 0, 0` | `\033[38;2;0;0;0m` |

### Color Reset
`\033[0m` — Always reset after colored output

### Usage Guidelines
- **Lime Green**: Headers, success messages, key identifiers (agent IDs, file paths)
- **White**: Standard output, body text, logs
- **Black Background**: Optional for high-contrast sections

---

## 🖼️ ASCII LOGO

### Placeholder Design
```
[Rounded "G" chat-bubble style emblem to be designed in Phase 4 - Stylize]
```

### Logo Specifications
- **Style**: Rounded "G" resembling a chat bubble
- **Color**: Lime Green (#BFF549)
- **Size**: Fits within 80-column terminal width
- **Display**: System boot sequence, `--help` output, main menu

---

## 🚀 BOOT SEQUENCE

### Initialization Output
```
[ASCII LOGO in Lime Green]

GLAIDO OMNI-NEXUS v1.0.0
Autonomous AI Infrastructure

[●] Protocol 0: Initialization... ✓
[●] Architecture Layer... ✓
[●] Navigation Layer... ✓
[●] Tools Layer... ✓
[●] Agent Registry... ✓

System Online — Ready for Command
```

### Styling
- Progress indicators: `[●]` in Lime Green
- Checkmarks: `✓` in Lime Green
- Error indicators: `✗` in White
- Cyberpunk aesthetic: Clean, structured, professional

---

## 🔧 CLI COMMAND STRUCTURE

### Main Entry Point
**File**: `cli/main.py`

**Usage**:
```bash
python cli/main.py <command> [options]
```

### Command Categories
```
General:
  init         Initialize new Omni-Nexus instance
  status       Show system health and metrics
  help         Display help information

Agents:
  agent create --spec=<file>    Create new agent
  agent list                    List all agents
  agent delete --id=<id> --confirm  Delete agent
  agent inspect --id=<id>       Show agent details

Tools:
  tool run --id=<id> --input=<json>  Execute tool directly
  tool list                          List all tools
  tool test --id=<id>                Run tool tests

Workflows:
  workflow trigger --id=<id>    Start workflow
  workflow status --id=<id>     Check workflow status

System:
  repair                        Run self-annealing diagnostics
  logs --service=<name>         View system logs
  clean                         Clean .tmp/ directory
```

---

## 📊 OUTPUT FORMATTING

### Standard Success Output
```python
# Example implementation (Phase 4)
from cli.display.formatter import success, info, error

def command_handler():
    info("Creating new agent...")
    # ... execution
    success("Agent 'agent_example' created successfully")
    info(f"Location: agents/agent_example/")
```

**Output**:
```
[●] Creating new agent...
[✓] Agent 'agent_example' created successfully
    Location: agents/agent_example/
```

### Error Output
```python
error("Agent ID 'agent_example' already exists")
info("Use --force to overwrite")
```

**Output**:
```
[✗] Agent ID 'agent_example' already exists
    Use --force to overwrite
```

---

## 📋 VERBOSE LOGGING MODE

### Behavioral Rule
User specified: "verbose logging enabled"

### Implementation
All commands support `--verbose` flag:
```bash
python cli/main.py agent create --spec=spec.json --verbose
```

**Output includes**:
- Step-by-step execution
- Internal tool calls
- Schema validation details
- File operations
- Timing information

**Example**:
```
[●] agent create --spec=spec.json
[→] Validating spec.json against agent_config schema...
[→] Schema validation passed
[→] Routing to tools/agents/agent_spawner.py...
[→] Creating directory: agents/agent_example/
[→] Writing config.json (256 bytes)
[→] Writing manifest.md (512 bytes)
[→] Writing behavior.py (1024 bytes)
[→] Updating agents/_registry.json...
[✓] Agent 'agent_example' created successfully (0.34s)
```

---

## 🛡️ DESTRUCTIVE ACTION CONFIRMATION

### Behavioral Rule
"Never delete or overwrite user data without explicit confirmation"

### Implementation
All destructive commands require `--confirm` flag:
```bash
# ❌ FAILS
python cli/main.py agent delete --id=agent_example

# Output:
# [✗] Destructive action requires --confirm flag
# [!] This will permanently delete: agents/agent_example/

# ✅ SUCCEEDS
python cli/main.py agent delete --id=agent_example --confirm
```

---

## 🎯 FORMATTER IMPLEMENTATION SPEC

### File
`cli/display/formatter.py`

### Functions (Phase 4)
```python
def lime_green(text: str) -> str:
    """Wrap text in lime green ANSI codes."""
    return f"\033[38;2;191;245;73m{text}\033[0m"

def white(text: str) -> str:
    """Wrap text in white ANSI codes."""
    return f"\033[38;2;255;255;255m{text}\033[0m"

def success(message: str) -> None:
    """Print success message with lime green checkmark."""
    print(f"{lime_green('[✓]')} {white(message)}")

def error(message: str) -> None:
    """Print error message with white X."""
    print(f"{white('[✗]')} {white(message)}")

def info(message: str) -> None:
    """Print info message with lime green bullet."""
    print(f"{lime_green('[●]')} {white(message)}")

def header(text: str) -> None:
    """Print large lime green header."""
    print(f"\n{lime_green('='*60)}")
    print(f"{lime_green(text.center(60))}")
    print(f"{lime_green('='*60)}\n")
```

---

## 📊 PROGRESS INDICATORS

### Spinner (for long-running operations)
```
[●] Generating agent... ⠋
[●] Generating agent... ⠙
[●] Generating agent... ⠹
[●] Generating agent... ⠸
[✓] Agent generated successfully
```

### Progress Bar (for multi-step workflows)
```
[●] Agent Creation Workflow
    [████████████────────] 60% (3/5 steps complete)
    Current: Writing behavior.py
```

---

**Last Updated**: 2026-02-13T20:58:39+05:00  
**Status**: Specification defined — ready for Phase 4 (Stylize) implementation
