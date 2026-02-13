"""
Tool: Logger
Purpose: Centralized logging with structured output and brand color support
Category: utilities
Created: 2026-02-13T21:04:24+05:00
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Literal

# Ensure .tmp/logs/ exists
LOGS_DIR = Path(__file__).parent.parent.parent / ".tmp" / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# ANSI color codes (brand identity)
LIME_GREEN = "\033[38;2;191;245;73m"
WHITE = "\033[38;2;255;255;255m"
RESET = "\033[0m"

LogLevel = Literal["info", "warning", "error", "critical", "success"]


def log(
    message: str,
    level: LogLevel = "info",
    service: str = "system",
    metadata: dict = None
) -> None:
    """
    Log a message to both console and file.
    
    Args:
        message: Log message content
        level: Log severity level
        service: Service name (system, agents, tools, navigation, etc.)
        metadata: Additional context to include in log
    """
    timestamp = datetime.now().isoformat()
    
    # Structured log entry
    log_entry = {
        "timestamp": timestamp,
        "level": level,
        "service": service,
        "message": message,
        "metadata": metadata or {}
    }
    
    # Write to appropriate log file
    log_file = LOGS_DIR / f"{service}.log"
    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    # Console output with color coding
    _print_console(message, level)


def _print_console(message: str, level: LogLevel) -> None:
    """Print colored console output based on log level."""
    
    if level == "success":
        icon = f"{LIME_GREEN}[✓]{RESET}"
    elif level == "error" or level == "critical":
        icon = f"{WHITE}[✗]{RESET}"
    elif level == "warning":
        icon = f"{WHITE}[!]{RESET}"
    else:  # info
        icon = f"{LIME_GREEN}[●]{RESET}"
    
    print(f"{icon} {WHITE}{message}{RESET}")


def info(message: str, service: str = "system", metadata: dict = None) -> None:
    """Log info level message."""
    log(message, "info", service, metadata)


def success(message: str, service: str = "system", metadata: dict = None) -> None:
    """Log success level message."""
    log(message, "success", service, metadata)


def warning(message: str, service: str = "system", metadata: dict = None) -> None:
    """Log warning level message."""
    log(message, "warning", service, metadata)


def error(message: str, service: str = "system", metadata: dict = None) -> None:
    """Log error level message."""
    log(message, "error", service, metadata)


def critical(message: str, service: str = "system", metadata: dict = None) -> None:
    """Log critical level message."""
    log(message, "critical", service, metadata)


def get_logs(service: str = "system", lines: int = 50) -> list[dict]:
    """
    Retrieve recent log entries.
    
    Args:
        service: Service name to retrieve logs for
        lines: Number of recent lines to retrieve
        
    Returns:
        List of log entry dictionaries
    """
    log_file = LOGS_DIR / f"{service}.log"
    
    if not log_file.exists():
        return []
    
    # Read last N lines
    with log_file.open("r", encoding="utf-8") as f:
        all_lines = f.readlines()
        recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
    
    # Parse JSON entries
    logs = []
    for line in recent_lines:
        try:
            logs.append(json.loads(line.strip()))
        except json.JSONDecodeError:
            continue
    
    return logs


if __name__ == "__main__":
    # CLI testing
    if len(sys.argv) > 1:
        test_message = " ".join(sys.argv[1:])
        info(test_message)
        success(test_message)
        warning(test_message)
        error(test_message)
    else:
        info("Logger initialized successfully")
        success("Test success message")
        warning("Test warning message")
        error("Test error message")
