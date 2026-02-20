"""
Python Package Validator — Verification Tool

Purpose: Verify that required Python packages are importable in the current
         environment using importlib.util.find_spec() only.

Category: dependency
Layer: Tools (Layer 3) — A.N.T. Layer Separation, Invariant #2
Created: 2026-02-19T21:17:39+05:00
B.L.A.S.T. Phase: Link (L)

Invariant Compliance:
  #1  Offline-First    — no network calls, importlib only
  #2  A.N.T. Separation — tool in tools/core/, not navigation/
  #4  Local Execution  — CLI-triggered or standalone only
  #5  Deterministic    — same env = same output
  #6  No Meta-Exec     — find_spec() used, no bare import, no pip calls

Standalone execution:
  python tools/core/python_package_check.py

Integration (Architect phase only — DO NOT wire yet):
  Append to tools list in verification_orchestrator.py:
  ("python_packages", workspace / "tools/core/python_package_check.py")
"""

import sys
import json
import time
import importlib.util
from datetime import datetime, timezone, timedelta


# ─────────────────────────────────────────────────────────────
# REQUIRED PACKAGES — MVP scope (phase-1: stdlib only)
# Extend only via a new B.L.A.S.T. cycle (Blueprint → Link).
# ─────────────────────────────────────────────────────────────
REQUIRED_PACKAGES = [
    "json",
    "pathlib",
    "importlib",
    "subprocess",
    "sys",
    "io",
    "argparse",
]


def _now_iso() -> str:
    """Return current local timestamp in ISO-8601 format."""
    # Hardcoded +05:00 offset consistent with system timezone
    tz = timezone(timedelta(hours=5))
    return datetime.now(tz).strftime("%Y-%m-%dT%H:%M:%S+05:00")


def check_packages() -> dict:
    """
    Check importability of each package in REQUIRED_PACKAGES.

    Uses importlib.util.find_spec() exclusively.
    Does NOT execute import statements or any package code.
    Returns a structured result dict.
    """
    details = []
    present_count = 0
    missing_names = []

    for pkg in REQUIRED_PACKAGES:
        try:
            spec = importlib.util.find_spec(pkg)
            if spec is not None:
                details.append({"name": pkg, "status": "present"})
                present_count += 1
            else:
                details.append({"name": pkg, "status": "missing"})
                missing_names.append(pkg)
        except (ModuleNotFoundError, ValueError):
            # ModuleNotFoundError: package namespace not findable
            # ValueError:          find_spec called with empty/invalid name
            details.append({"name": pkg, "status": "missing"})
            missing_names.append(pkg)

    return {
        "details": details,
        "present_count": present_count,
        "missing_names": missing_names,
    }


def run_check() -> dict:
    """
    Execute all package checks and build the verification output.

    Output conforms to verification_output_format.md individual tool schema
    and the directive-specified format for the `dependency` category.
    """
    try:
        start_time = time.time()
        result = check_packages()

        total = len(REQUIRED_PACKAGES)
        present = result["present_count"]
        missing = total - present
        missing_names = result["missing_names"]
        all_present = missing == 0

        # Status: "ready" only when every package is importable
        status = "ready" if all_present else "error"

        # Human-readable message
        if all_present:
            message = (
                f"All {total} required packages are importable "
                f"via importlib.util.find_spec()"
            )
        else:
            message = (
                f"{missing} of {total} required package(s) not importable: "
                + ", ".join(missing_names)
            )

        report = {
            "category": "python_packages",
            "status": status,
            "executed": True,
            "timestamp": _now_iso(),
            "metrics": {
                "duration_ms": round((time.time() - start_time) * 1000, 2)
            },
            "results": {
                "packages_checked": total,
                "packages_present": present,
                "packages_missing": missing,
                "details": result["details"],
            },
            "message": message,
            "actionable": not all_present,
            "remediation": (
                "Install missing packages manually or verify your Python "
                "installation includes the expected stdlib modules. "
                "See architecture/sops/verification_operational_guidelines.md "
                "§Package Dependency Failures for full guidance."
            ),
        }

        return report

    except Exception as exc:  # noqa: BLE001 — outer safety net
        # Never surface a bare exception; always emit valid JSON
        return {
            "category": "dependency",
            "status": "error",
            "executed": False,
            "timestamp": _now_iso(),
            "results": {
                "packages_checked": 0,
                "packages_present": 0,
                "packages_missing": 0,
                "details": [],
            },
            "message": f"Tool execution error: {exc}",
            "actionable": True,
            "remediation": (
                "Inspect the error message above. Ensure Python ≥ 3.8 and "
                "that importlib is available in the active interpreter."
            ),
        }


if __name__ == "__main__":
    output = run_check()
    print(json.dumps(output, indent=2, sort_keys=True))
    sys.exit(0 if output["status"] == "ready" else 1)
