"""Utility functions for gitignore file operations."""


def merge_gitignore(existing_content: str, template_content: str) -> tuple[str, int]:
    """
    Merge gitignore template with existing content, avoiding duplicates.
    
    Args:
        existing_content: Current .gitignore file content
        template_content: Template content from gitignore.io
        
    Returns:
        tuple: (merged_content, number_of_added_patterns)
            - merged_content: The merged gitignore content
            - number_of_added_patterns: Count of new patterns added
    """
    # Parse existing content - normalize entries (ignore comments/empty lines)
    existing_lines = {
        line.strip()
        for line in existing_content.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    
    # Parse template content
    template_lines = template_content.splitlines()
    
    # Compute missing entries - patterns in template not in existing
    missing_lines = [
        line
        for line in template_lines
        if line.strip() and not line.lstrip().startswith("#") and line.strip() not in existing_lines
    ]
    
    # If no new patterns, return original content
    if not missing_lines:
        return existing_content, 0
    
    # Build merged content with new patterns
    merged = existing_content.rstrip("\n")
    merged += "\n\n# === Patterns added by mcp-gitignore ===\n"
    merged += "\n".join(missing_lines) + "\n"
    
    return merged, len(missing_lines)
