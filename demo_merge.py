#!/usr/bin/env python3
"""
Manual test to demonstrate the improved .gitignore merging functionality.
This script shows how the merge function works in practice.
"""

from mcp_tools.utils import merge_gitignore

def demo_merge_functionality():
    """Demonstrate the merge functionality with examples."""
    
    print("=" * 80)
    print("DEMONSTRATION: Improved .gitignore Merging")
    print("=" * 80)
    
    # Example 1: Empty existing file
    print("\n" + "=" * 80)
    print("Example 1: Starting with empty .gitignore")
    print("=" * 80)
    existing = ""
    template = """# Python
*.pyc
__pycache__/
.env
"""
    merged, count = merge_gitignore(existing, template)
    print(f"Added {count} patterns")
    print("\nMerged content:")
    print(merged)
    
    # Example 2: No overlapping patterns
    print("\n" + "=" * 80)
    print("Example 2: Merging with no overlap")
    print("=" * 80)
    existing = """# My custom rules
*.log
tmp/
"""
    template = """# Python
*.pyc
__pycache__/
.env
"""
    merged, count = merge_gitignore(existing, template)
    print(f"Added {count} patterns")
    print("\nMerged content:")
    print(merged)
    
    # Example 3: Some overlapping patterns
    print("\n" + "=" * 80)
    print("Example 3: Merging with partial overlap")
    print("=" * 80)
    existing = """# Existing patterns
*.pyc
my-custom-file.txt
node_modules/
"""
    template = """# Python template
*.pyc
__pycache__/
.env
*.py[cod]
"""
    merged, count = merge_gitignore(existing, template)
    print(f"Added {count} patterns (*.pyc already existed, so it wasn't added again)")
    print("\nMerged content:")
    print(merged)
    
    # Example 4: All patterns already exist
    print("\n" + "=" * 80)
    print("Example 4: All patterns already exist - no changes needed")
    print("=" * 80)
    existing = """# Complete Python setup
*.pyc
__pycache__/
.env
"""
    template = """# Python
*.pyc
__pycache__/
.env
"""
    merged, count = merge_gitignore(existing, template)
    print(f"Added {count} patterns (all already existed)")
    print("\nMerged content (unchanged):")
    print(merged)
    print("\nNotice: No '# === Patterns added by mcp-gitignore ===' section was added!")
    
    # Example 5: Real-world scenario
    print("\n" + "=" * 80)
    print("Example 5: Real-world scenario - adding Python patterns to existing Node.js project")
    print("=" * 80)
    existing = """# Node.js
node_modules/
npm-debug.log
package-lock.json
.env

# My custom rules
*.bak
tmp/
"""
    template = """# Python
*.pyc
__pycache__/
*.py[cod]
*$py.class
.Python
build/
dist/
*.egg-info/
.env
venv/
"""
    merged, count = merge_gitignore(existing, template)
    print(f"Added {count} patterns")
    print(f"Note: .env already existed, so it wasn't duplicated")
    print("\nMerged content:")
    print(merged)
    
    print("\n" + "=" * 80)
    print("Key Benefits:")
    print("=" * 80)
    print("✓ No duplicate entries")
    print("✓ Preserves existing structure and comments")
    print("✓ Only adds new patterns under a clear header")
    print("✓ If no new patterns, returns unchanged content")
    print("✓ Ignores comments and empty lines when comparing")
    print("=" * 80)


if __name__ == "__main__":
    demo_merge_functionality()
