#!/usr/bin/env python3
"""
Verification that our implementation matches the reference implementation
from the issue requirements.
"""

from mcp_tools.utils import merge_gitignore


def reference_implementation(existing_content: str, template_content: str) -> str:
    """
    Reference implementation from the issue.
    """
    existing_lines = {
        line.strip()
        for line in existing_content.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    template_lines = template_content.splitlines()
    missing_lines = [
        line
        for line in template_lines
        if line.strip() and not line.lstrip().startswith("#") and line not in existing_lines
    ]
    if not missing_lines:
        return existing_content
    merged = existing_content.rstrip("\n")
    merged += "\n\n# === Patterns added by mcp-gitignore ===\n"
    merged += "\n".join(missing_lines) + "\n"
    return merged


def verify_implementation():
    """
    Verify our implementation produces the same results as the reference.
    """
    print("=" * 80)
    print("VERIFICATION: Implementation vs Reference")
    print("=" * 80)
    
    test_cases = [
        {
            "name": "Empty existing",
            "existing": "",
            "template": "*.pyc\n__pycache__/\n.env\n"
        },
        {
            "name": "No duplicates",
            "existing": "node_modules/\npackage-lock.json\n",
            "template": "*.pyc\n__pycache__/\n.env\n"
        },
        {
            "name": "All duplicates",
            "existing": "*.pyc\n__pycache__/\n.env\n",
            "template": "*.pyc\n__pycache__/\n.env\n"
        },
        {
            "name": "Partial duplicates",
            "existing": "*.pyc\nnode_modules/\n",
            "template": "*.pyc\n__pycache__/\n.env\n"
        },
        {
            "name": "With comments",
            "existing": "# Python\n*.pyc\n# Node\nnode_modules/\n",
            "template": "*.pyc\n__pycache__/\n"
        },
    ]
    
    all_match = True
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['name']}")
        print("-" * 80)
        
        # Run both implementations
        reference_result = reference_implementation(test["existing"], test["template"])
        our_result, _ = merge_gitignore(test["existing"], test["template"])
        
        # Compare results
        if reference_result == our_result:
            print("✅ MATCH - Both implementations produce identical output")
        else:
            print("❌ MISMATCH - Outputs differ")
            print("\nReference output:")
            print(repr(reference_result))
            print("\nOur output:")
            print(repr(our_result))
            all_match = False
    
    print("\n" + "=" * 80)
    if all_match:
        print("✅ SUCCESS: All test cases match the reference implementation!")
        print("=" * 80)
        print("\nOur implementation correctly follows the specification:")
        print("1. ✅ Parses existing content, normalizing entries")
        print("2. ✅ Parses template content")
        print("3. ✅ Computes missing entries")
        print("4. ✅ Returns unchanged if no missing lines")
        print("5. ✅ Appends only new patterns under clear header")
        print("6. ✅ Uses exact header: '# === Patterns added by mcp-gitignore ==='")
        return True
    else:
        print("❌ FAILURE: Some test cases don't match")
        return False


if __name__ == "__main__":
    success = verify_implementation()
    exit(0 if success else 1)
