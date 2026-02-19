"""
CLI Display: ANSI Formatter
Purpose: Brand color constants and terminal formatting utilities
Category: cli/display
Created: 2026-02-13T21:05:00+05:00
"""

import sys
from typing import Literal

# Brand colors from gemini.md
LIME_GREEN = "\033[38;2;191;245;73m"
WHITE = "\033[38;2;255;255;255m"
BLACK = "\033[38;2;0;0;0m"

# Control codes
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
UNDERLINE = "\033[4m"

# Background colors
BG_BLACK = "\033[48;2;0;0;0m"
BG_LIME = "\033[48;2;191;245;73m"

ColorChoice = Literal["lime", "white", "black"]


def color(text: str, color_name: ColorChoice = "white", bold: bool = False) -> str:
    """
    Apply brand color to text.
    
    Args:
        text: Text to colorize
        color_name: Brand color name
        bold: Apply bold formatting
        
    Returns:
        ANSI-formatted string
    """
    color_map = {
        "lime": LIME_GREEN,
        "white": WHITE,
        "black": BLACK
    }
    
    color_code = color_map[color_name]
    bold_code = BOLD if bold else ""
    
    return f"{bold_code}{color_code}{text}{RESET}"


def header(text: str) -> str:
    """Create bold lime header."""
    return color(text, "lime", bold=True)


# Convenience color functions
def lime(text: str, bold: bool = False) -> str:
    """Apply lime color to text."""
    return color(text, "lime", bold=bold)


def white(text: str, bold: bool = False) -> str:
    """Apply white color to text."""
    return color(text, "white", bold=bold)


def black(text: str, bold: bool = False) -> str:
    """Apply black color to text."""
    return color(text, "black", bold=bold)


# Semantic colors — per cli_branding_guidelines.md §Semantic Color Extensions
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"


def red(text: str) -> str:
    """Apply red color (error state) per branding spec."""
    return f"{RED}{text}{RESET}"


def yellow(text: str) -> str:
    """Apply yellow color (warning state) per branding spec."""
    return f"{YELLOW}{text}{RESET}"


def cyan(text: str) -> str:
    """Apply cyan color (info state) per branding spec."""
    return f"{CYAN}{text}{RESET}"


def bold(text: str) -> str:
    """Make text bold."""
    return f"{BOLD}{WHITE}{text}{RESET}"


def dim(text: str) -> str:
    """Make text dim."""
    return f"{DIM}{WHITE}{text}{RESET}"


def box(text: str, style: Literal["solid", "double"] = "solid") -> str:
    """
    Create a box around text.
    
    Args:
        text: Text to box
        style: Box style (solid or double)
        
    Returns:
        Boxed text string
    """
    lines = text.split("\n")
    max_len = max(len(line) for line in lines)
    
    if style == "double":
        top = f"{LIME_GREEN}╔{'═' * (max_len + 2)}╗{RESET}"
        bottom = f"{LIME_GREEN}╚{'═' * (max_len + 2)}╝{RESET}"
        line_template = f"{LIME_GREEN}║{WHITE} {{:<{max_len}}} {LIME_GREEN}║{RESET}"
    else:
        top = f"{LIME_GREEN}┌{'─' * (max_len + 2)}┐{RESET}"
        bottom = f"{LIME_GREEN}└{'─' * (max_len + 2)}┘{RESET}"
        line_template = f"{LIME_GREEN}│{WHITE} {{:<{max_len}}} {LIME_GREEN}│{RESET}"
    
    result = [top]
    for line in lines:
        result.append(line_template.format(line))
    result.append(bottom)
    
    return "\n".join(result)


def separator(length: int = 50, char: str = "─") -> str:
    """Create horizontal separator."""
    return f"{LIME_GREEN}{char * length}{RESET}"


def bullet(text: str, symbol: str = "•") -> str:
    """Create bullet point."""
    return f"{LIME_GREEN}{symbol}{WHITE} {text}{RESET}"


def status_icon(status: Literal["success", "error", "warning", "info"]) -> str:
    """
    Get status icon.
    
    Args:
        status: Status type
        
    Returns:
        Colored icon
    """
    icons = {
        "success": f"{LIME_GREEN}[✓]{RESET}",
        "error": f"{WHITE}[✗]{RESET}",
        "warning": f"{WHITE}[!]{RESET}",
        "info": f"{LIME_GREEN}[●]{RESET}"
    }
    return icons[status]


# Status indicator functions
def success_indicator(text: str) -> str:
    """Create success indicator with checkmark."""
    return f"{status_icon('success')} {lime(text)}"


def error_indicator(text: str) -> str:
    """Create error indicator with X."""
    return f"{status_icon('error')} {white(text)}"


def warning_indicator(text: str) -> str:
    """Create warning indicator with exclamation."""
    return f"{status_icon('warning')} {white(text)}"


def info_indicator(text: str) -> str:
    """Create info indicator with bullet."""
    return f"{status_icon('info')} {white(text)}"


def progress_bar(current: int, total: int, width: int = 30) -> str:
    """
    Create ASCII progress bar.
    
    Args:
        current: Current progress
        total: Total items
        width: Bar width in characters
        
    Returns:
        Progress bar string
    """
    if total == 0:
        percentage = 0
    else:
        percentage = int((current / total) * 100)
    
    filled = int((current / total) * width) if total > 0 else 0
    bar = "█" * filled + "░" * (width - filled)
    
    return f"{LIME_GREEN}[{bar}]{WHITE} {percentage}%{RESET}"


def banner() -> str:
    """
    Generate Omni-Nexus ASCII banner.
    
    Returns:
        Multi-line ASCII art banner
    """
    logo = f"""{LIME_GREEN}
    ╔═══════════════════════════════════════════╗
    ║                                           ║
    ║     ██████╗ ███╗   ███╗███╗   ██╗██╗     ║
    ║    ██╔═══██╗████╗ ████║████╗  ██║██║     ║
    ║    ██║   ██║██╔████╔██║██╔██╗ ██║██║     ║
    ║    ██║   ██║██║╚██╔╝██║██║╚██╗██║██║     ║
    ║    ╚██████╔╝██║ ╚═╝ ██║██║ ╚████║██║     ║
    ║     ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝     ║
    ║                                           ║
    ║{WHITE}         GLAIDO OMNI-NEXUS v1.0         {LIME_GREEN}║
    ║{WHITE}      Autonomous AI Infrastructure      {LIME_GREEN}║
    ║                                           ║
    ╚═══════════════════════════════════════════╝
{RESET}"""
    return logo


def create_banner(text: str, width: int = 50) -> str:
    """Create a banner with centered text."""
    padding = (width - len(text)) // 2
    border = "═" * width
    
    return f"""{LIME_GREEN}╔{border}╗
║{' ' * padding}{WHITE}{text}{LIME_GREEN}{' ' * (width - len(text) - padding)}║
╚{border}╝{RESET}"""


def create_section_divider(width: int = 60) -> str:
    """Create a section divider line."""
    return f"{LIME_GREEN}{'─' * width}{RESET}"


def create_table(headers: list, rows: list) -> str:
    """Create a simple table from headers and rows."""
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            # Strip ANSI codes to get real length
            clean_cell = cell.replace(LIME_GREEN, "").replace(WHITE, "").replace(RESET, "")
            clean_cell = clean_cell.replace(BOLD, "").replace(DIM, "")
            # Remove other potential ANSI codes
            import re
            clean_cell = re.sub(r'\033\[[0-9;]+m', '', str(cell))
            col_widths[i] = max(col_widths[i], len(clean_cell))
    
    # Build table
    lines = []
    
    # Header row
    header_cells = [f"{lime(h, bold=True):^{col_widths[i]}}" for i, h in enumerate(headers)]
    lines.append("  " + "  ".join(header_cells))
    
    # Separator
    lines.append("  " + "  ".join(["─" * w for w in col_widths]))
    
    # Data rows
    for row in rows:
        # For each cell, pad considering ANSI codes
        formatted_cells = []
        for i, cell in enumerate(row):
            # Get visible length (without ANSI)
            import re
            visible = re.sub(r'\033\[[0-9;]+m', '', str(cell))
            padding_needed = col_widths[i] - len(visible)
            formatted_cells.append(str(cell) + " " * padding_needed)
        lines.append("  " + "  ".join(formatted_cells))
    
    return "\n".join(lines)


def create_bullet_list(items: list) -> str:
    """Create a bullet list."""
    return "\n".join([f"  • {item}" for item in items])


if __name__ == "__main__":
    # Demo all formatting
    print(banner())
    print()
    print(header("SYSTEM STATUS"))
    print(separator())
    print(bullet("Architecture layer initialized"))
    print(bullet("Navigation layer online"))
    print(bullet("Tools layer ready"))
    print()
    print(f"{status_icon('success')} {color('All systems operational', 'white')}")
    print(f"{status_icon('info')} {color('Agents: 3 active', 'white')}")
    print()
    print(progress_bar(7, 10))
    print()
    print(box("This is a boxed message\nWith multiple lines", style="double"))
