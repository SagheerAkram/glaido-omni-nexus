# Verification Display Contract — Specification

> **Purpose**: Define visual presentation standards for verification system output  
> **Phase**: Stylize (Phase 4)  
> **Status**: Documentation Only — No Implementation Code

---

## Core Principle

The verification display contract specifies **how verification JSON output should be rendered visually** in the CLI interface. This document is purely descriptive and defines presentation requirements without executable logic.

---

## Input Contract

### Data Source

**Input**: JSON output from `verification_orchestrator.py`

**Schema Reference**: `architecture/specifications/verification_output_format.md`

**Key Fields for Display**:
- `overall_status`: System readiness determination
- `system_ready`: Boolean flag
- `verifications`: Individual tool results
- `execution_order`: Tool execution sequence
- `timestamp`: Verification execution time

---

## Display States Overview

The verification display has three primary states based on `overall_status`:

1. **Success State**: All verifications passed (`overall_status = "ready"`)
2. **Warning State**: Non-critical issues detected (degraded but operational)
3. **Failure State**: Critical failures detected (`overall_status = "not_ready"`)

---

## Success State Display

### Trigger Condition

**When**: `overall_status = "ready"` AND all tool statuses are `ready` or `healthy`

---

### Visual Structure

**Top-Level Banner**:
Large success indicator with system status

**Summary Section**:
High-level overview of verification results

**Details Section**:
Individual tool results in tabular or list format

**Completion Message**:
Confirmation of system readiness

---

### Content Requirements

**Banner Text**:
- "SYSTEM VERIFICATION COMPLETE"
- Primary success indicator (checkmark symbol)
- Overall status in prominent position

**Summary Content**:
- "Overall Status: READY"
- "System Ready: Yes"
- Timestamp of verification
- Number of tools verified

**Details Content**:
For each verification tool:
- Tool category name
- Status indicator (success symbol)
- Key metrics or findings
- Execution confirmation

**Completion Content**:
- "System is operational and ready for use"
- No action items required

---

### Tone and Language

**Characteristics**:
- Confident and affirmative
- Concise and professional
- No ambiguity or hedging
- Action-oriented conclusion

**Examples**:
- "All verifications passed"
- "System ready for operation"
- "No issues detected"

**Prohibited**:
- Overly enthusiastic language ("Great!", "Awesome!")
- Unnecessary verbosity
- Vague or uncertain statements

---

## Warning State Display

### Trigger Condition

**When**: System operational but with non-critical issues

**Example Scenarios**:
- Filesystem integrity returns `degraded` status
- Temp directory writable but low disk space
- Agent registry has zero agents (not critical)

---

### Visual Structure

**Top-Level Banner**:
Warning indicator with qualified status

**Summary Section**:
Overall status with warning context

**Details Section**:
Individual tool results, highlighting warnings

**Advisory Section**:
Non-critical issues and recommendations

**Completion Message**:
System operational with notes

---

### Content Requirements

**Banner Text**:
- "SYSTEM VERIFICATION COMPLETE WITH WARNINGS"
- Warning indicator symbol
- Overall status with qualification

**Summary Content**:
- "Overall Status: OPERATIONAL (with warnings)"
- "System Ready: Yes (degraded)"
- Warning count and categories
- Timestamp

**Details Content**:
For each verification tool:
- Tool category name
- Status indicator (success or warning)
- Issues detected (if any)
- Impact assessment

**Advisory Content**:
- List of non-critical issues
- Recommended actions (non-urgent)
- Context for each warning
- Impact on system functionality

**Completion Content**:
- "System operational but review recommended"
- Advisory to address warnings when convenient

---

### Tone and Language

**Characteristics**:
- Balanced and informative
- Cautionary but not alarming
- Actionable recommendations
- Clear distinction from critical errors

**Examples**:
- "Non-critical issues detected"
- "System functional with reduced capacity"
- "Review recommended but not required"

**Prohibited**:
- Alarmist language
- Ambiguous severity
- Mixing warnings with errors

---

## Failure State Display

### Trigger Condition

**When**: `overall_status = "not_ready"` OR any critical tool returns error status

**Example Scenarios**:
- Python version below requirement
- Missing required directories
- Registry file corrupt or missing
- Tool execution timeout or crash

---

### Visual Structure

**Top-Level Banner**:
Prominent error indicator with failure status

**Summary Section**:
Overall failure status with error count

**Error Details Section**:
Critical failures listed with full context

**Impact Assessment Section**:
Explanation of system operability impact

**Remediation Section**:
Required actions to resolve failures

**Completion Message**:
System not ready, action required

---

### Content Requirements

**Banner Text**:
- "SYSTEM VERIFICATION FAILED"
- Error indicator symbol
- Critical failure count

**Summary Content**:
- "Overall Status: NOT READY"
- "System Ready: No"
- Number of critical failures
- Number of tools that failed
- Timestamp

**Error Details Content**:
For each failed verification:
- Tool category name
- Failure indicator
- Specific error message
- Error context (what was checked)
- Expected vs. actual state

**Impact Assessment Content**:
- "System cannot operate until issues resolved"
- Specific capabilities affected
- Dependencies blocked by failures

**Remediation Content**:
For each error:
- Required corrective action
- Step-by-step resolution if available
- Priority/urgency level
- Estimated effort

**Completion Content**:
- "System initialization blocked"
- "Resolve errors before proceeding"

---

### Tone and Language

**Characteristics**:
- Direct and unambiguous
- Actionable and specific
- Urgent but professional
- Solution-oriented

**Examples**:
- "Critical failure detected"
- "System cannot proceed"
- "Immediate action required"
- "Resolve issue by [specific action]"

**Prohibited**:
- Panic-inducing language
- Vague error descriptions
- Blame attribution
- Non-actionable messages

---

## Individual Tool Result Display

### Per-Tool Structure

Each verification tool result should display:

**Tool Identifier**:
- Category name (e.g., "Local Dependencies")
- Clear, human-readable label

**Status Indicator**:
- Visual symbol (checkmark, warning, error)
- Status text (READY, DEGRADED, ERROR)

**Summary Line**:
- One-line description of result
- Key metric or finding

**Details Expansion** (optional):
- Detailed findings for this tool
- Specific checks performed
- Sub-component statuses

---

### Local Dependencies Display

**Minimum Display**:
- "Local Dependencies: [STATUS]"
- Python version detected
- Module availability summary

**Expanded Display** (if issues):
- Missing modules listed
- Version comparison (required vs. actual)
- Filesystem writability status

---

### Filesystem Integrity Display

**Minimum Display**:
- "Filesystem Integrity: [STATUS]"
- Overall health assessment
- Critical file/directory status

**Expanded Display** (if issues):
- Missing directories listed
- Unreadable files identified
- Architecture immutability status
- Temp directory writability

---

### Schema Validation Display

**Minimum Display**:
- "Schema Validation: [STATUS]"
- Validator availability
- Documentation presence

**Expanded Display** (if issues):
- Validator file status
- Import errors (if any)
- Missing documentation

---

### Agent Registry Display

**Minimum Display**:
- "Agent Registry: [STATUS]"
- Registry file existence
- Agent count

**Expanded Display** (if issues):
- JSON validity status
- Structure validation errors
- Write permission status
- Backup functionality

---

## Layout Patterns

### Compact Layout

**Use Case**: Quick status check, all verifications passed

**Structure**:
- Single-line banner
- One-line status per tool
- Simple completion message

**Total Height**: ~10-15 lines

---

### Standard Layout

**Use Case**: Default display, mixed results

**Structure**:
- Multi-line banner with box-drawing
- Summary section
- Tool results in table format
- Completion message

**Total Height**: ~20-30 lines

---

### Detailed Layout

**Use Case**: Failures or warnings present

**Structure**:
- Prominent banner
- Executive summary
- Detailed tool results
- Error/warning details
- Remediation section
- Completion message

**Total Height**: Variable (30-100+ lines depending on errors)

---

## Spacing and Alignment

### Vertical Spacing

**Section Separation**: Single blank line between major sections

**Sub-section Separation**: No blank line between related items

**Banner Spacing**: Blank line before and after banners

---

### Horizontal Alignment

**Labels**: Left-aligned

**Status Indicators**: Right-aligned or inline after label

**Details**: Indented 2 spaces from parent item

**Tables**: Column-aligned with consistent padding

---

## Data Presentation Formats

### Timestamp Display

**Format**: Human-readable local time

**Example**: "Verified at: 2026-02-13 21:40:00 +05:00"

**Placement**: Summary section or footer

---

### Boolean Values

**True States**: "Yes", "Pass", "Available", "Functional"

**False States**: "No", "Fail", "Missing", "Non-functional"

**Avoid**: Raw "true"/"false" text

---

### Numeric Values

**Counts**: Display with context (e.g., "4 of 4 tools passed")

**Percentages**: When relevant (e.g., "100% success rate")

**Versions**: Show as-is (e.g., "Python 3.11.0")

---

### Lists

**Bullet Style**: Use bullet character (•) for unordered lists

**Numbered Style**: Use numbers for sequential items

**Nested Lists**: Indent with 2 spaces per level

---

## Status Indicator Symbols

### Success Symbols

**Primary**: ✅ (checkmark in box)

**Alternative**: ✓ (simple checkmark)

**Usage**: Tool passed, system ready, verification success

---

### Warning Symbols

**Primary**: ⚠️ (warning sign)

**Alternative**: ! (exclamation)

**Usage**: Non-critical issues, degraded state, advisory

---

### Error Symbols

**Primary**: ❌ (cross mark)

**Alternative**: ✗ (simple X)

**Usage**: Critical failure, system not ready, blocking error

---

### Info Symbols

**Primary**: ℹ️ (information)

**Alternative**: → (arrow for directional info)

**Usage**: Neutral information, context, notes

---

## Progressive Disclosure

### Collapsed View

**Default Behavior**: Show high-level status only

**Content**:
- Overall status
- Tool status summary
- No error details

**Use Case**: Quick status check, passing verification

---

### Expanded View

**Trigger**: Failures or warnings detected, or verbose flag enabled

**Content**:
- All collapsed view content
- Detailed error messages
- Remediation steps
- Full JSON output (optional)

**Use Case**: Debugging, failure analysis

---

## Accessibility Requirements

### Plain Text Compatibility

All information must be comprehensible without:
- Color coding
- Unicode symbols
- Box-drawing characters

**Fallback**: Symbols replaced with text equivalents

**Example**:
- `✅` becomes `[PASS]`
- `❌` becomes `[FAIL]`
- `⚠️` becomes `[WARN]`

---

### Screen Reader Compatibility

**Requirements**:
- Status text always accompanies symbols
- Tables have clear headers
- Lists have proper hierarchy
- No information conveyed by color alone

---

## Error Message Guidelines

### Error Presentation

**Structure**:
```
Category: [Tool Name]
Status: ERROR
Issue: [Specific problem]
Expected: [What should be]
Actual: [What was found]
Action: [How to fix]
```

**Emphasis**:
- Issue and Action statements most prominent
- Context (Expected/Actual) secondary but clear

---

### Helpful Context

**Include**:
- File paths when relevant
- Version numbers when relevant
- Specific values checked
- Link to documentation if available

**Exclude**:
- Stack traces in standard view (move to debug)
- Internal implementation details
- Overly technical jargon

---

## Consistency Rules

### Cross-Tool Consistency

All tool results must:
- Use identical status indicator format
- Follow same layout pattern
- Apply same emphasize hierarchy
- Use consistent terminology

---

### Multi-Run Consistency

Display should:
- Look identical for identical results
- Not randomize order or presentation
- Maintain stable layout across runs

---

## Future Enhancements

### Interactive Elements

**Possible Future Features**:
- Collapsible/expandable sections
- Interactive error resolution wizards
- Clickable remediation links

**Current Status**: Not implemented, text-only display

---

### Real-Time Updates

**Possible Future Features**:
- Live progress indicators during verification
- Streaming tool results as they complete
- Dynamic status updates

**Current Status**: Static output after completion

---

## Summary

Verification display contract ensures:
- **Clarity**: Unambiguous status communication
- **Actionability**: Clear next steps for failures
- **Consistency**: Uniform presentation across states
- **Accessibility**: Readable without advanced terminal features
- **Professionalism**: Enterprise-appropriate tone and format

This specification serves as the reference for implementing CLI display logic in future phases without modifying verification tools or orchestrator.

---

**Last Updated**: 2026-02-13T21:40:00+05:00  
**Status**: Stylize specification — awaiting CLI implementation
