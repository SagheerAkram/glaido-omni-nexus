#!/usr/bin/env python3
import os
import re
from pathlib import Path

# ==============================================================================
# Phase D: Global Markdown Polish Utility
# ------------------------------------------------------------------------------
# Purpose: Scans all markdown files in the architecture/ directory.
# Ensures every file has a "# <Title>" and a "## Purpose" section.
# Normalizes header spacing without deleting or rewriting user content.
# Conforms to the "Offline Execution" and "No Runtime Modification" invariants.
# ==============================================================================

def polish_markdown_file(filepath: Path) -> bool:
    """Reads, polishes, and writes a single markdown file if changes are needed."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        lines = content.splitlines()
        if not lines:
            return False
            
        modified = False
        new_lines = []
        
        # Ensure # Title on first line
        title_match = re.match(r'^#\s+(.+)$', lines[0])
        if not title_match:
            # Check if there's a title anywhere
            found_title = False
            for i, line in enumerate(lines):
                if line.startswith('# '):
                    lines.insert(0, lines.pop(i))
                    found_title = True
                    modified = True
                    break
            if not found_title:
                lines.insert(0, f"# {filepath.stem.replace('_', ' ').title()}")
                modified = True
                
        # Ensure ## Purpose section exists
        has_purpose = any(line.upper().startswith('## PURPOSE') for line in lines)
        if not has_purpose:
            # Insert ## Purpose right after the Title (and any immediate blank lines)
            insert_idx = 1
            while insert_idx < len(lines) and lines[insert_idx].strip() == '':
                insert_idx += 1
            
            lines.insert(insert_idx, "")
            lines.insert(insert_idx + 1, "## Purpose")
            lines.insert(insert_idx + 2, "This document serves as an architectural component of the Glaido Omni-Nexus. Content to be defined.")
            lines.insert(insert_idx + 3, "")
            modified = True
            
        # Normalize spacing between headers
        content_joined = '\n'.join(lines)
        
        # Ensure exactly one blank line before and after headers (except start of file)
        # (Simplified regex normalization for safety)
        normalized = re.sub(r'\n{3,}(#.*)', r'\n\n\1', content_joined)
        normalized = re.sub(r'(#.*)\n{3,}', r'\1\n\n', normalized)
        
        if normalized != content_joined:
            modified = True
            content_joined = normalized
            
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content_joined)
            return True
            
        return False
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def run_polish():
    workspace_root = Path(__file__).resolve().parent.parent.parent
    arch_dir = workspace_root / "architecture"
    
    if not arch_dir.exists():
        print(f"Architecture directory not found at {arch_dir}")
        return
        
    print("Initiating Phase D: Global Markdown Polish...")
    modified_count = 0
    scanned_count = 0
    
    for md_file in arch_dir.rglob("*.md"):
        scanned_count += 1
        if polish_markdown_file(md_file):
            print(f"[POLISHED] {md_file.relative_to(workspace_root)}")
            modified_count += 1
            
    print("-" * 40)
    print(f"Phase D Complete. Scanned: {scanned_count} | Polished: {modified_count}")

if __name__ == "__main__":
    # NOTE: Execution is currently DORMANT. 
    # Run this file manually to apply the polish safely.
    run_polish()
