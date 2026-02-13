"""
CLI Display Package

Provides terminal formatting and rendering utilities.
"""

from cli.display.formatter import (
    # Color functions
    lime,
    white,
    red,
    yellow,
    cyan,
    bold,
    dim,
    
    # Status indicators
    success_indicator,
    warning_indicator,
    error_indicator,
    info_indicator,
    
    # Formatting functions
    create_banner,
    create_section_divider,
    create_table,
    create_bullet_list,
    
    # Color control
    disable_color,
    enable_color
)

from cli.display.verification_renderer import (
    render_verification_results,
    render_from_file,
    render_from_stdin
)

__all__ = [
    # Color functions
    'lime',
    'white',
    'red',
    'yellow',
    'cyan',
    'bold',
    'dim',
    
    # Status indicators
    'success_indicator',
    'warning_indicator',
    'error_indicator',
    'info_indicator',
    
    # Formatting
    'create_banner',
    'create_section_divider',
    'create_table',
    'create_bullet_list',
    
    # Color control
    'disable_color',
    'enable_color',
    
    # Verification rendering
    'render_verification_results',
    'render_from_file',
    'render_from_stdin'
]
