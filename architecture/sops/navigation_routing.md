# Navigation Routing — SOP

> **Purpose**: Define orchestration logic for task routing and agent coordination  
> **Layer**: Architecture (SOP)  
> **Updated**: 2026-02-13T20:58:39+05:00

---

## 🎯 CORE PRINCIPLE

> **"Navigation should be boring."**

Navigation layer is a **thin orchestrator** that routes tasks to appropriate tools/agents. It contains **NO business logic**, only decision trees and routing tables.

---

## 🏗️ ARCHITECTURE

### Layer Responsibility
- **Navigation** (Layer 2): Decision routing only
- **Tools** (Layer 3): All actual execution
- **Forbidden**: Data transformation, business logic, heavy computation in navigation

### Components

**Current Active Components** (v1.0):
```
navigation/
└── orchestrator/
    └── verification_orchestrator.py  → Baseline linear verification executor
```

**Future Components** (Post-Stabilization):
```
navigation/
├── orchestrator/
│   ├── verification_orchestrator.py → ✅ Baseline linear executor (ACTIVE)
│   ├── task_router.py     → Routes incoming tasks (future)
│   ├── agent_coordinator.py → Manages agent lifecycle (future)
│   └── workflow_manager.py  → Coordinates multi-step workflows (future)
├── routing/
│   ├── decision_tree.py   → Implements routing decisions (future)
│   ├── priority_queue.py  → Task priority management (future)
│   └── context_handler.py → Session context storage (future)
└── data_flow/
    ├── input_validator.py → Schema validation (future)
    ├── output_formatter.py → Format tool outputs (future)
    └── stream_manager.py   → Handle data streams (future)
```

---

## 🎯 BASELINE ORCHESTRATOR (v1.0)

### Verification Orchestrator

**File**: `navigation/orchestrator/verification_orchestrator.py`  
**Derived From**: `architecture/sops/link_verification_protocol.md`  
**Purpose**: Baseline linear executor for system readiness verification

**Characteristics**:
- ✅ **Linear execution** — No decision trees or branching
- ✅ **Sequential only** — Tools run in fixed order
- ✅ **No routing logic** — Direct subprocess calls
- ✅ **Minimal aggregation** — Simple all-pass/all-fail status
- ✅ **Stateless** — No session or context management

**Execution Order** (from Link SOP):
1. `tools/core/local_dependency_check.py`
2. `tools/core/filesystem_integrity_check.py`
3. `tools/core/schema_validator_stub.py`
4. `tools/agents/registry_readiness_check.py`

**Output**: Aggregated JSON report with `overall_status` and individual tool results

**Navigation Layer Lock**:
> This orchestrator is the **ONLY** active navigation component in v1.0.  
> No additional routers, managers, queues, or context handlers until stabilization complete.

---

## 📊 ROUTING DECISION SCHEMA

All routing decisions use this standardized format (defined in `gemini.md`):

```json
{
  "task_id": "unique_task_identifier",
  "route_type": "agent_spawn|tool_call|workflow_trigger|error_recovery",
  "target": "agent_id or tool_id",
  "payload": {
    "...": "data to pass to target"
  },
  "fallback": "fallback_target_if_primary_fails"
}
```

**Note**: Routing schema not yet used by baseline orchestrator (v1.0). Will be implemented in future navigation components.

---

## 🔀 ROUTING LOGIC

### Step 1: Task Classification
**Tool**: `navigation/routing/decision_tree.py`

**Input**: Task request from CLI or external trigger  
**Output**: Route type determination

**Classification Rules**:
- Agent already exists + task matches capability → `tool_call`
- Agent doesn't exist + need new capability → `agent_spawn`
- Multi-step process → `workflow_trigger`
- Tool failure detected → `error_recovery`

**Example**:
```python
# Pseudocode only — actual implementation in Phase 3 (Architect)
def classify_task(task_request):
    if task_request.type == "create_agent":
        return "agent_spawn"
    elif task_request.type == "execute":
        return "tool_call"
    # ... more rules
```

---

### Step 2: Target Resolution
**Tool**: `navigation/orchestrator/task_router.py`

**Input**: Route type + task requirements  
**Output**: Specific target (agent ID or tool ID)

**Resolution Strategy**:
1. Check `agents/_registry.json` for matching capabilities
2. If multiple matches → select by priority/availability
3. If no match → route to `agent_spawner` to create new agent
4. If target unavailable → use fallback

---

### Step 3: Payload Preparation
**Tool**: `navigation/data_flow/input_validator.py`

**Actions**:
1. Validate payload against `gemini.md` schemas
2. Transform into target-specific format
3. Inject context (session ID, timestamp, etc.)

**Validation**: All payloads validated **before** routing

---

### Step 4: Execution Delegation
**Tool**: `navigation/orchestrator/agent_coordinator.py` or direct tool call

**Actions**:
1. Pass payload to target
2. Monitor execution (don't intervene)
3. Capture output
4. Route to output formatter

**Critical Rule**: Navigation **NEVER** executes logic. It only calls tools/agents.

---

## 🔄 WORKFLOW COORDINATION

### Multi-Step Workflows
**Tool**: `navigation/orchestrator/workflow_manager.py`

**Purpose**: Coordinate sequences of tool calls

**Example Workflow**: Agent Generation
1. Route to `tools/agents/agent_spawner.py` → Validate spec
2. Route to `tools/agents/agent_spawner.py` → Create folder
3. Route to `tools/agents/agent_spawner.py` → Generate files
4. Route to `tools/agents/agent_spawner.py` → Update registry
5. Collect results → Format output

**Navigation's Role**: Sequential routing only. Each tool executes independently.

---

## ⚠️ ERROR RECOVERY ROUTING

### Failure Detection
If tool returns error status:
1. Capture error context
2. Log to `.tmp/logs/system.log`
3. Route to appropriate recovery tool
4. If recovery fails → escalate to self-annealing repair

### Recovery Routes
```
Tool failure → tools/core/diagnostics.py → Analyze error
Diagnostics → tools/[category]/repair_[tool].py → Attempt fix
Repair success → Retry original task
Repair failure → Log to findings.md, notify user
```

---

## 🛡️ ANTI-PATTERNS (FORBIDDEN)

### ❌ Data Transformation in Navigation
```python
# FORBIDDEN
def route_task(data):
    transformed = data.upper()  # ❌ Business logic in navigation
    return call_tool(transformed)
```

### ✅ Correct Pattern
```python
# CORRECT
def route_task(data):
    return call_tool("tools/data/transform.py", data)  # ✅ Delegate to tool
```

---

### ❌ Complex Logic in Navigation
```python
# FORBIDDEN
def decide_target(task):
    if task.priority > 5 and task.type == "urgent":
        # ... 50 lines of decision logic ❌
```

### ✅ Correct Pattern
```python
# CORRECT
def decide_target(task):
    return decision_tree.classify(task)  # ✅ Calls external tool
```

---

## 📋 IMPLEMENTATION CHECKLIST (Phase 3)

Navigation implementation must:
- [ ] Use routing schemas from `gemini.md`
- [ ] Validate all inputs before routing
- [ ] Log routing decisions to `.tmp/logs/`
- [ ] Never perform business logic
- [ ] Always delegate to tools layer
- [ ] Handle failures gracefully
- [ ] Stay "boring" (simple, predictable)

---

**Last Updated**: 2026-02-13T21:33:00+05:00  
**Status**: Baseline orchestrator implemented (verification_orchestrator.py) — navigation layer locked to single component
