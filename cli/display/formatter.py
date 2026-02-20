"""
CLI Display: ANSI Formatter
Purpose: Brand color constants and terminal formatting utilities
Category: cli/display
Created: 2026-02-13T21:05:00+05:00
"""

import sys
from typing import Literal, List, Any

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

COLOR_ENABLED = True


def disable_color() -> None:
    """Disable ANSI color formatting globally."""
    global COLOR_ENABLED
    COLOR_ENABLED = False


def enable_color() -> None:
    """Enable ANSI color formatting globally."""
    global COLOR_ENABLED
    COLOR_ENABLED = True


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
    if not COLOR_ENABLED:
        return text

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
    if not COLOR_ENABLED:
        return text
    return f"{RED}{text}{RESET}"


def yellow(text: str) -> str:
    """Apply warning color per branding spec."""
    if not COLOR_ENABLED:
        return text
    return f"{YELLOW}{text}{RESET}"


def cyan(text: str) -> str:
    """Apply info color per branding spec."""
    if not COLOR_ENABLED:
        return text
    return f"{CYAN}{text}{RESET}"


def bold(text: str) -> str:
    """Make text bold."""
    if not COLOR_ENABLED:
        return text
    return f"{BOLD}{WHITE}{text}{RESET}"


def dim(text: str) -> str:
    """Make text dim."""
    if not COLOR_ENABLED:
        return text
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
    
    if not COLOR_ENABLED:
        result = ["┌" + "─" * (max_len + 2) + "┐"]
        for line in lines:
            result.append(f"│ {line:<{max_len}} │")
        result.append("└" + "─" * (max_len + 2) + "┘")
        return "\n".join(result)

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
    if not COLOR_ENABLED:
        return char * length
    return f"{LIME_GREEN}{char * length}{RESET}"


def bullet(text: str, symbol: str = "•") -> str:
    """Create bullet point."""
    if not COLOR_ENABLED:
        return f"{symbol} {text}"
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

    if not COLOR_ENABLED:
        fallback = {
            "success": "[OK]",
            "error": "[FAILED]",
            "warning": "[WARN]",
            "info": "[INFO]"
        }
        return fallback[status]
        
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
    
    if not COLOR_ENABLED:
        return f"[{bar}] {percentage}%"
    
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
    if not COLOR_ENABLED:
        return logo.replace(LIME_GREEN, "").replace(WHITE, "").replace(RESET, "")

    return logo


def create_banner(text: str, width: int = 50) -> str:
    """Create a banner with centered text."""
    padding = (width - len(text)) // 2
    border = "═" * width
    
    if not COLOR_ENABLED:
        return f"╔{border}╗\n║{' ' * padding}{text}{' ' * (width - len(text) - padding)}║\n╚{border}╝"

    return f"""{LIME_GREEN}╔{border}╗
║{' ' * padding}{WHITE}{text}{LIME_GREEN}{' ' * (width - len(text) - padding)}║
╚{border}╝{RESET}"""


def create_section_divider(width: int = 60) -> str:
    """Create a section divider line."""
    if not COLOR_ENABLED:
        return "─" * width
    return f"{LIME_GREEN}{'─' * width}{RESET}"


def kv_pair(key: str, value: Any, align: int = 0) -> str:
    """
    Format a key-value pair.
    
    Args:
        key: The key string
        value: The value string or object
        align: Optional padding to align values
        
    Returns:
        Formatted string like: "Key    : Value"
    """
    padding = max(0, align - len(key))
    key_part = f"{lime(key)}{' ' * padding}"
    
    if not COLOR_ENABLED:
        return f"{key}{' ' * padding}: {value}"
        
    return f"{key_part}{dim(':')} {white(str(value))}"


def create_table(headers: List[str], rows: List[List[Any]]) -> str:
    """Create a premium Unicode table from headers and rows."""
    import re
    
    def strip_ansi(text: str) -> str:
        text = str(text)
        text = text.replace(LIME_GREEN, "").replace(WHITE, "").replace(RESET, "")
        text = text.replace(BOLD, "").replace(DIM, "")
        return re.sub(r'\033\[[0-9;]+m', '', text)

    # Calculate column widths
    col_widths = [len(strip_ansi(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(strip_ansi(cell)))
    
    # Add padding to widths (1 space each side)
    col_widths = [w + 2 for w in col_widths]
    
    lines = []
    
    if not COLOR_ENABLED:
        top_left, top_mid, top_right = "+", "+", "+"
        mid_left, mid_mid, mid_right = "+", "+", "+"
        bot_left, bot_mid, bot_right = "+", "+", "+"
        bot_v, mid_v, top_v = "|", "|", "|"
        horiz = "-"
        border_color, header_color = "", ""
    else:
        top_left, top_mid, top_right = "┌", "┬", "┐"
        mid_left, mid_mid, mid_right = "├", "┼", "┤"
        bot_left, bot_mid, bot_right = "└", "┴", "┘"
        bot_v, mid_v, top_v = "│", "│", "│"
        horiz = "─"
        border_color = LIME_GREEN
        header_color = LIME_GREEN

    # Helpers
    def format_row(cells, make_bold=False):
        formatted = []
        for i, cell in enumerate(cells):
            clean_length = len(strip_ansi(cell))
            padding = col_widths[i] - clean_length - 1  # -1 for left padding
            # Format cell with 1 left space, right space padding
            if make_bold and COLOR_ENABLED:
                formatted_cell = f" {bold(str(cell))}{' ' * padding}"
            else:
                formatted_cell = f" {cell}{' ' * padding}"
            formatted.append(formatted_cell)
        
        separator = f"{border_color}{mid_v}{RESET}" if COLOR_ENABLED else mid_v
        left_edge = f"{border_color}{top_v}{RESET}" if COLOR_ENABLED else top_v
        right_edge = f"{border_color}{top_v}{RESET}" if COLOR_ENABLED else top_v
        return f"  {left_edge}{separator.join(formatted)}{right_edge}"

    # Draw Top Line
    top_segments = [horiz * w for w in col_widths]
    top_line = f"  {border_color}{top_left}{top_mid.join(top_segments)}{top_right}{RESET}"
    lines.append(top_line if COLOR_ENABLED else top_line.replace(LIME_GREEN, "").replace(RESET, ""))
    
    # Draw Headers
    lines.append(format_row(headers, make_bold=True))
    
    # Draw Separator
    mid_segments = [horiz * w for w in col_widths]
    mid_line = f"  {border_color}{mid_left}{mid_mid.join(mid_segments)}{mid_right}{RESET}"
    lines.append(mid_line if COLOR_ENABLED else mid_line.replace(LIME_GREEN, "").replace(RESET, ""))
    
    # Draw Rows
    for row in rows:
        lines.append(format_row(row))
        
    # Draw Bottom Line
    bot_segments = [horiz * w for w in col_widths]
    bot_line = f"  {border_color}{bot_left}{bot_mid.join(bot_segments)}{bot_right}{RESET}"
    lines.append(bot_line if COLOR_ENABLED else bot_line.replace(LIME_GREEN, "").replace(RESET, ""))
    
    return "\n".join(lines)


def create_bullet_list(items: List[Any]) -> str:
    """Create a bullet list."""
    return "\n".join([f"  {bullet(str(item))}" for item in items])


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
