"""
Unit tests for gitignore merge functionality.
"""

import pytest
from mcp_tools.utils import merge_gitignore


def test_merge_with_empty_existing():
    """Test merging when existing content is empty."""
    existing = ""
    template = "*.pyc\n__pycache__/\n.env\n"
    
    merged, count = merge_gitignore(existing, template)
    
    assert count == 3
    assert "# === Patterns added by mcp-gitignore ===" in merged
    assert "*.pyc" in merged
    assert "__pycache__/" in merged
    assert ".env" in merged


def test_merge_with_no_duplicates():
    """Test merging when there are no overlapping patterns."""
    existing = "node_modules/\npackage-lock.json\n"
    template = "*.pyc\n__pycache__/\n.env\n"
    
    merged, count = merge_gitignore(existing, template)
    
    assert count == 3
    assert "node_modules/" in merged
    assert "package-lock.json" in merged
    assert "# === Patterns added by mcp-gitignore ===" in merged
    assert "*.pyc" in merged
    assert "__pycache__/" in merged
    assert ".env" in merged


def test_merge_with_all_duplicates():
    """Test merging when all patterns already exist."""
    existing = "*.pyc\n__pycache__/\n.env\n"
    template = "*.pyc\n__pycache__/\n.env\n"
    
    merged, count = merge_gitignore(existing, template)
    
    assert count == 0
    assert merged == existing  # Should return unchanged
    assert "# === Patterns added by mcp-gitignore ===" not in merged


def test_merge_with_partial_duplicates():
    """Test merging when some patterns overlap."""
    existing = "*.pyc\nnode_modules/\n"
    template = "*.pyc\n__pycache__/\n.env\n"
    
    merged, count = merge_gitignore(existing, template)
    
    assert count == 2
    assert "*.pyc" in merged
    assert "node_modules/" in merged
    assert "# === Patterns added by mcp-gitignore ===" in merged
    assert "__pycache__/" in merged
    assert ".env" in merged


def test_merge_ignores_comments_in_existing():
    """Test that comments in existing content are preserved but not compared."""
    existing = "# Python\n*.pyc\n# Node\nnode_modules/\n"
    template = "*.pyc\n__pycache__/\n"
    
    merged, count = merge_gitignore(existing, template)
    
    assert count == 1  # Only __pycache__/ is new
    assert "# Python" in merged
    assert "# Node" in merged
    assert "__pycache__/" in merged


def test_merge_ignores_comments_in_template():
    """Test that comments in template are not added as patterns."""
    existing = "*.pyc\n"
    template = "# Created by gitignore.io\n*.pyc\n__pycache__/\n# End\n"
    
    merged, count = merge_gitignore(existing, template)
    
    assert count == 1  # Only __pycache__/ is new
    assert "# Created by gitignore.io" not in merged
    assert "# End" not in merged
    assert "__pycache__/" in merged


def test_merge_ignores_empty_lines():
    """Test that empty lines are handled correctly."""
    existing = "*.pyc\n\n\nnode_modules/\n"
    template = "*.pyc\n\n__pycache__/\n\n.env\n"
    
    merged, count = merge_gitignore(existing, template)
    
    assert count == 2  # __pycache__/ and .env
    assert "__pycache__/" in merged
    assert ".env" in merged


def test_merge_handles_whitespace():
    """Test that whitespace in patterns is normalized."""
    existing = "*.pyc  \n  node_modules/\n"
    template = "*.pyc\n__pycache__/\n"
    
    merged, count = merge_gitignore(existing, template)
    
    # *.pyc with trailing space should match *.pyc without
    assert count == 1  # Only __pycache__/ is new


def test_merge_preserves_existing_structure():
    """Test that the existing file structure is preserved."""
    existing = "# My custom rules\n*.log\n\n# Dependencies\nnode_modules/\n"
    template = "*.pyc\n__pycache__/\n"
    
    merged, count = merge_gitignore(existing, template)
    
    assert count == 2
    # Check that existing content appears first
    assert merged.index("# My custom rules") < merged.index("# === Patterns added by mcp-gitignore ===")
    assert merged.index("*.log") < merged.index("*.pyc")
    assert merged.index("node_modules/") < merged.index("__pycache__/")


def test_merge_with_trailing_newlines():
    """Test that trailing newlines are handled properly."""
    existing = "*.pyc\nnode_modules/\n\n\n"
    template = "__pycache__/\n.env\n"
    
    merged, count = merge_gitignore(existing, template)
    
    assert count == 2
    # Should have proper formatting
    assert merged.endswith("\n")
    assert "# === Patterns added by mcp-gitignore ===" in merged


def test_merge_real_world_scenario():
    """Test a realistic scenario with multiple templates."""
    existing = """# Custom rules
*.log
tmp/

# Python
*.pyc
__pycache__/
"""
    
    # Simulating a Python + Node template from gitignore.io
    template = """# Python
*.pyc
__pycache__/
*.py[cod]
*$py.class

# Node
node_modules/
npm-debug.log
"""
    
    merged, count = merge_gitignore(existing, template)
    
    # Should add: *.py[cod], *$py.class, node_modules/, npm-debug.log
    assert count == 4
    assert "*.py[cod]" in merged
    assert "*$py.class" in merged
    assert "node_modules/" in merged
    assert "npm-debug.log" in merged
    # Existing content should be preserved
    assert "# Custom rules" in merged
    assert "*.log" in merged
    assert "tmp/" in merged


def test_merge_case_sensitive():
    """Test that pattern matching is case-sensitive."""
    existing = "*.Pyc\n"
    template = "*.pyc\n"
    
    merged, count = merge_gitignore(existing, template)
    
    # These should be treated as different patterns
    assert count == 1
    assert "*.Pyc" in merged
    assert "*.pyc" in merged


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
