"""
Verification Renderer Module

Converts verification orchestrator JSON output into visual terminal display.
Implements verification_display_contract.md specifications.
"""

import json
from datetime import datetime
import formatter


# ============================================================================
# MAIN RENDERING FUNCTION
# ============================================================================

def render_verification_results(verification_json):
    """
    Render verification results to terminal.
    
    Args:
        verification_json: Dict or JSON string from verification orchestrator
        
    Returns:
        str: Formatted terminal output
    """
    # Parse JSON if string
    if isinstance(verification_json, str):
        data = json.loads(verification_json)
    else:
        data = verification_json
    
    # Determine display state
    overall_status = data.get("overall_status", "not_ready")
    
    if overall_status == "ready":
        return _render_success_state(data)
    elif _has_warnings(data):
        return _render_warning_state(data)
    else:
        return _render_failure_state(data)


# ============================================================================
# SUCCESS STATE RENDERING
# ============================================================================

def _render_success_state(data):
    """Render success state (all verifications passed)"""
    lines = []
    
    # Banner
    lines.append("")
    lines.append(formatter.create_banner("GLAIDO OMNI-NEXUS — ENGINEERING VERIFICATION CORE", width=70))
    lines.append("")
    
    # Summary
    lines.append(formatter.kv_pair("Overall Status", "READY", align=18))
    lines.append(formatter.kv_pair("System Ready", "Yes", align=18))
    
    timestamp = data.get("timestamp", "")
    if timestamp:
        lines.append(formatter.kv_pair("Verified at", timestamp, align=18))
    
    lines.append("")
    
    # Tool results table
    headers = ["Component", "Status", "Details"]
    rows = _build_verification_rows(data.get("verifications", {}))
    
    if rows:
        lines.append(formatter.create_table(headers, rows))
    
    lines.append("")
    
    # Completion message
    lines.append(formatter.success_indicator("System is operational and ready for use"))
    lines.append("")
    
    return "\n".join(lines)


def _build_verification_rows(verifications):
    """Build table rows for all states"""
    rows = []
    
    # Define display order and labels
    # Stylize Phase (2026-02-19): python_packages added at position 3
    # Expansion Cycle 4: Execution Intelligence labels added
    tool_labels = {
        "local_dependencies":   "Local Dependencies",
        "workspace_hygiene":    "Workspace Hygiene",
        "python_syntax":        "Python Syntax",
        "ant_boundary":         "A.N.T Boundary",
        "pipeline_integrity":   "Pipeline Integrity",
        "architecture_links":   "Architecture Links",
        "filesystem_integrity": "Filesystem Integrity",
        "python_packages":      "Python Packages",
        "schema_validation":    "Schema Validation",
        "agent_registry":       "Agent Registry",
    }
    
    for category, label in tool_labels.items():
        if category in verifications:
            tool_data = verifications[category]
            status = tool_data.get("status", "unknown")
            
            # Build status indicator
            if status in ["ready", "healthy"]:
                status_text = formatter.success_indicator(status.upper())
            else:
                status_text = status.upper()
            
            # Build details
            details = _extract_details(category, tool_data)
            
            rows.append([label, status_text, details])
    
    return rows


def _extract_details(category, tool_data):
    """Extract key details for table display"""
    status = tool_data.get("status", "unknown")
    
    # Fallback to error message if not ready
    if status not in ["ready", "healthy"] and tool_data.get("message"):
        return tool_data.get("message")
        
    if category == "local_dependencies":
        py_ver = tool_data.get("python_version", {}).get("current", "")
        return f"Python {py_ver}" if py_ver else "All OK"

    elif category == "filesystem_integrity":
        return "All directories present"

    elif category == "workspace_hygiene":
        return "Workspace structure verified"

    elif category == "python_syntax":
        return "No syntax errors detected"

    elif category == "python_packages":
        # Reads from results.packages_checked — no execution, presentation only
        results = tool_data.get("results", {})
        total   = results.get("packages_checked", 0)
        present = results.get("packages_present", total)
        return f"All {total} packages importable" if present == total else f"{present}/{total} present"

    elif category == "schema_validation":
        return "Validator importable"

    elif category == "agent_registry":
        count = tool_data.get("agent_count", 0)
        return f"{count} agents"
        
    elif category == "ant_boundary":
        return "Layer boundaries respected"

    elif category == "pipeline_integrity":
        return "All tools registered"

    elif category == "architecture_links":
        return "No broken architecture links"

    return "OK"


# ============================================================================
# WARNING STATE RENDERING
# ============================================================================

def _render_warning_state(data):
    """Render warning state (operational with non-critical issues)"""
    lines = []
    
    # Banner
    lines.append("")
    lines.append(formatter.create_banner("GLAIDO OMNI-NEXUS — ENGINEERING VERIFICATION CORE", width=70))
    lines.append("")
    
    # Summary
    lines.append(formatter.kv_pair("Overall Status", "OPERATIONAL (with warnings)", align=18))
    lines.append(formatter.kv_pair("System Ready", "Yes (degraded)", align=18))
    
    timestamp = data.get("timestamp", "")
    if timestamp:
        lines.append(formatter.kv_pair("Verified at", timestamp, align=18))
    
    lines.append("")
    
    # Tool results
    headers = ["Component", "Status", "Details"]
    rows = _build_verification_rows(data.get("verifications", {}))
    
    if rows:
        lines.append(formatter.create_table(headers, rows))
    
    lines.append("")
    
    # Advisory section
    warnings = _extract_warnings(data.get("verifications", {}))
    if warnings:
        lines.append(formatter.lime("Advisories:"))
        lines.append("")
        for warning in warnings:
            lines.append(formatter.warning_indicator(warning))
    
    lines.append("")
    lines.append(formatter.info_indicator("System operational but review recommended"))
    lines.append("")
    
    return "\n".join(lines)


def _has_warnings(data):
    """Check if verification has warnings (degraded but operational)"""
    verifications = data.get("verifications", {})
    
    for tool_data in verifications.values():
        status = tool_data.get("status", "")
        if status == "degraded":
            return True
    
    return False


def _extract_warnings(verifications):
    """Extract warning messages from verification data"""
    warnings = []
    
    for category, tool_data in verifications.items():
        status = tool_data.get("status", "")
        
        if status == "degraded":
            warnings.append(f"{category.replace('_', ' ').title()}: Degraded state detected")
    
    return warnings


# ============================================================================
# FAILURE STATE RENDERING
# ============================================================================

def _render_failure_state(data):
    """Render failure state (critical failures detected)"""
    lines = []
    
    # Banner
    lines.append("")
    lines.append(formatter.create_banner("GLAIDO OMNI-NEXUS — ENGINEERING VERIFICATION CORE", width=70))
    lines.append("")
    
    # Summary
    lines.append(formatter.kv_pair("Overall Status", formatter.red("NOT READY"), align=18))
    lines.append(formatter.kv_pair("System Ready", formatter.red("No"), align=18))
    
    # Count failures
    failure_count = _count_failures(data.get("verifications", {}))
    lines.append(formatter.kv_pair("Critical Failures", str(failure_count), align=18))
    
    timestamp = data.get("timestamp", "")
    if timestamp:
        lines.append(formatter.kv_pair("Verified at", timestamp, align=18))
    
    lines.append("")
    
    # Tool results table
    headers = ["Component", "Status", "Details"]
    rows = _build_verification_rows(data.get("verifications", {}))
    
    if rows:
        lines.append(formatter.create_table(headers, rows))
        
    lines.append("")
    
    # Print error details
    has_errors = False
    for category, tool_data in data.get("verifications", {}).items():
        if tool_data.get("status") not in ["ready", "healthy"]:
            error_details = _extract_error_details(category, tool_data)
            if error_details:
                if not has_errors:
                    lines.append(formatter.lime("Error Details:"))
                    lines.append("")
                    has_errors = True
                
                label = category.replace("_", " ").title()
                lines.append(f"  {formatter.red(label)}:")
                for detail in error_details:
                    lines.append(f"    • {detail}")
    
    if has_errors:
        lines.append("")
    
    # Impact assessment
    lines.append(formatter.lime("Impact:"))
    lines.append(formatter.error_indicator("System cannot operate until issues resolved"))
    lines.append("")
    
    # Remediation
    remediation_steps = _extract_remediation(data.get("verifications", {}))
    if remediation_steps:
        lines.append(formatter.lime("Required Actions:"))
        lines.append("")
        for step in remediation_steps:
            lines.append(f"  • {step}")
    
    lines.append("")
    lines.append(formatter.error_indicator("Resolve errors before proceeding"))
    lines.append("")
    
    return "\n".join(lines)


def _count_failures(verifications):
    """Count critical failures"""
    count = 0
    for tool_data in verifications.values():
        status = tool_data.get("status", "")
        if status not in ["ready", "healthy", "degraded"]:
            count += 1
    return count


def _extract_error_details(category, tool_data):
    """Extract error details for failure display"""
    details = []
    
    # Check for explicit error field
    if tool_data.get("error"):
        details.append(formatter.red(f"Error: {tool_data['error']}"))
    
    # Category-specific details
    if category == "local_dependencies":
        if not tool_data.get("python_version", {}).get("meets_requirement"):
            py_current = tool_data.get("python_version", {}).get("current", "unknown")
            py_required = tool_data.get("python_version", {}).get("required", "3.8")
            details.append(f"Python {py_current} does not meet requirement (≥{py_required})")
        
        missing_modules = tool_data.get("modules", {}).get("missing", [])
        if missing_modules:
            details.append(f"Missing modules: {', '.join(missing_modules)}")
    
    elif category == "filesystem_integrity":
        missing_dirs = tool_data.get("directories", {}).get("missing", [])
        if missing_dirs:
            details.append(f"Missing directories: {', '.join(missing_dirs)}")
        
        missing_files = tool_data.get("core_files", {}).get("missing", [])
        if missing_files:
            details.append(f"Missing files: {', '.join(missing_files)}")
    
    elif category == "workspace_hygiene":
        violations = tool_data.get("results", {}).get("violations", [])
        count = len(violations)
        details.append(f"{count} violation(s) detected")
        if violations:
            first = violations[0]
            details.append(f"Example: {first.get('path')} ({first.get('rule')})")
    
    elif category == "python_syntax":
        violations = tool_data.get("results", {}).get("violations", [])
        count = len(violations)
        details.append(f"{count} syntax error(s) detected")
        if violations:
            first = violations[0]
            line = first.get('line', '?')
            details.append(f"First error: {first.get('file')}:{line}")
    
    elif category == "python_packages":
        # Display contract: list each missing package with install advisory
        results      = tool_data.get("results", {})
        total        = results.get("packages_checked", 0)
        present      = results.get("packages_present", 0)
        missing_pkgs = [
            d["name"]
            for d in results.get("details", [])
            if d.get("status") == "missing"
        ]
        details.append(f"{present} of {total} packages importable")
        for pkg in missing_pkgs:
            details.append(formatter.red(f"\u2022 {pkg}") + " \u2014 not installed")
        if missing_pkgs:
            details.append(
                formatter.cyan("\u2192 Install missing packages manually (offline-first rule)")
            )
    
    elif category == "schema_validation":
        if not tool_data.get("validator_import", {}).get("importable"):
            details.append("Schema validator not importable")
    
    elif category == "agent_registry":
        if not tool_data.get("registry_exists"):
            details.append("Registry file not found")
        elif not tool_data.get("registry_valid_json"):
            details.append("Registry file is not valid JSON")

    elif category == "ant_boundary":
        violations = tool_data.get("results", {}).get("violations", [])
        count = len(violations)
        details.append(f"{count} violation(s) detected")
        if violations:
            first = violations[0]
            details.append(f"First error: {first.get('import')} in {first.get('file')}:{first.get('line')}")

    elif category == "pipeline_integrity":
        violations = tool_data.get("results", {}).get("violations", [])
        count = len(violations)
        details.append(f"{count} orphaned tool(s) detected")
        if violations:
            first = violations[0]
            details.append(f"First error: {first.get('file')} {first.get('reason')}")

    elif category == "architecture_links":
        violations = tool_data.get("results", {}).get("violations", [])
        count = len(violations)
        details.append(f"{count} broken link(s) detected")
        if violations:
            first = violations[0]
            details.append(f"First error: {first.get('broken_link')} in {first.get('file')}:{first.get('line')}")

    return details


def _extract_remediation(verifications):
    """Extract remediation steps for failures"""
    steps = []

    for category, tool_data in verifications.items():
        status = tool_data.get("status", "")

        if status not in ["ready", "healthy", "degraded"]:
            if category == "local_dependencies":
                if not tool_data.get("python_version", {}).get("meets_requirement"):
                    steps.append("Upgrade Python to version 3.8 or higher")

                missing_modules = tool_data.get("modules", {}).get("missing", [])
                if missing_modules:
                    steps.append(f"Install missing modules: {', '.join(missing_modules)}")

            elif category == "filesystem_integrity":
                missing_dirs = tool_data.get("directories", {}).get("missing", [])
                if missing_dirs:
                    steps.append("Create missing directories using project structure")

            elif category == "workspace_hygiene":
                if tool_data.get("remediation"):
                    steps.append(tool_data["remediation"])

            elif category == "python_syntax":
                if tool_data.get("remediation"):
                    steps.append(tool_data["remediation"])

            elif category == "python_packages":
                # Offline-first: direct user to manual installation only
                missing_pkgs = [
                    d["name"]
                    for d in tool_data.get("results", {}).get("details", [])
                    if d.get("status") == "missing"
                ]
                if missing_pkgs:
                    steps.append(
                        "Verify Python installation completeness — "
                        "missing: " + ", ".join(missing_pkgs)
                    )
                    steps.append(
                        "See architecture/sops/verification_operational_guidelines.md "
                        "\u00a7Package Dependency Failures for remediation guidance"
                    )

            elif category == "schema_validation":
                if not tool_data.get("validator_file", {}).get("exists"):
                    steps.append("Create tools/core/validator.py module")

            elif category == "agent_registry":
                if not tool_data.get("registry_exists"):
                    steps.append("Create agents/_registry.json file")

    return steps


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def _format_tool_status_line(category, tool_data, show_warnings=False, show_errors=False):
    """Format a single tool status line"""
    # Get human-readable label
    # Stylize Phase (2026-02-19): python_packages added
    labels = {
        "local_dependencies":   "Local Dependencies",
        "workspace_hygiene":    "Workspace Hygiene",
        "python_syntax":        "Python Syntax",
        "ant_boundary":         "A.N.T Boundary",
        "pipeline_integrity":   "Pipeline Integrity",
        "architecture_links":   "Architecture Links",
        "filesystem_integrity": "Filesystem Integrity",
        "python_packages":      "Python Packages",
        "schema_validation":    "Schema Validation",
        "agent_registry":       "Agent Registry",
    }
    
    label = labels.get(category, category.replace("_", " ").title())
    status = tool_data.get("status", "unknown")
    
    # Format status indicator
    if status in ["ready", "healthy"]:
        indicator = formatter.success_indicator(status.upper())
    elif status == "degraded":
        indicator = formatter.warning_indicator(status.upper())
    else:
        indicator = formatter.error_indicator(status.upper())
    
    return f"  {formatter.lime(label)}: {indicator}"


# ============================================================================
# CLI INTEGRATION
# ============================================================================

def render_from_file(json_file_path):
    """
    Render verification results from JSON file.
    
    Args:
        json_file_path: Path to JSON file
        
    Returns:
        str: Formatted output
    """
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    return render_verification_results(data)


def render_from_stdin():
    """
    Render verification results from stdin.
    
    Returns:
        str: Formatted output
    """
    import sys
    data = json.load(sys.stdin)
    return render_verification_results(data)
