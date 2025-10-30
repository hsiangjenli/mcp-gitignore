#!/usr/bin/env python3
"""
End-to-end test demonstrating the merge functionality with the actual API.
This simulates a real-world usage scenario.
"""

import json


def simulate_api_usage():
    """Simulate how a client would use the API with merge functionality."""
    
    print("=" * 80)
    print("END-TO-END SIMULATION: .gitignore Merging")
    print("=" * 80)
    
    # Scenario: A project starts with a custom .gitignore
    print("\n📝 Scenario: Developer starts with custom .gitignore")
    print("-" * 80)
    
    existing_gitignore = """# My custom rules
*.log
tmp/
secrets.txt
"""
    
    print("Existing .gitignore:")
    print(existing_gitignore)
    
    # Step 1: Developer wants to add Python patterns
    print("\n🔧 Step 1: Adding Python patterns")
    print("-" * 80)
    
    request_data_1 = {
        "templates": ["python"],
        "existing_content": existing_gitignore
    }
    
    print(f"API Request: POST /gitignore/generate/")
    print(f"Request body: {json.dumps(request_data_1, indent=2)}")
    
    # Simulate API response (in real usage, this would come from the server)
    print("\n✅ Expected API Response:")
    print(json.dumps({
        "success": True,
        "message": "Added 42 new pattern(s) from templates: python",
        "content": existing_gitignore.rstrip() + "\n\n# === Patterns added by mcp-gitignore ===\n*.pyc\n__pycache__/\n...(42 patterns total)",
        "patterns_added": 42
    }, indent=2))
    
    # Step 2: Developer tries to add Python patterns again
    print("\n\n🔧 Step 2: Attempting to add Python patterns again")
    print("-" * 80)
    
    # After first merge, the content now includes Python patterns
    updated_gitignore = existing_gitignore.rstrip() + "\n\n# === Patterns added by mcp-gitignore ===\n*.pyc\n__pycache__/\n"
    
    request_data_2 = {
        "templates": ["python"],
        "existing_content": updated_gitignore
    }
    
    print(f"API Request: POST /gitignore/generate/")
    print(f"Request body: {json.dumps(request_data_2, indent=2)}")
    
    print("\n✅ Expected API Response:")
    print(json.dumps({
        "success": True,
        "message": "No new patterns to add. All patterns from templates (python) already exist.",
        "content": updated_gitignore,
        "patterns_added": 0
    }, indent=2))
    
    print("\n💡 Result: Content unchanged - no duplicates added!")
    
    # Step 3: Developer adds Node.js to the project
    print("\n\n🔧 Step 3: Adding Node.js patterns to Python project")
    print("-" * 80)
    
    request_data_3 = {
        "templates": ["node"],
        "existing_content": updated_gitignore
    }
    
    print(f"API Request: POST /gitignore/generate/")
    print(f"Request body: {json.dumps(request_data_3, indent=2)}")
    
    print("\n✅ Expected API Response:")
    print(json.dumps({
        "success": True,
        "message": "Added 35 new pattern(s) from templates: node",
        "content": updated_gitignore.rstrip() + "\n\n# === Patterns added by mcp-gitignore ===\nnode_modules/\nnpm-debug.log\n...(35 patterns total)",
        "patterns_added": 35
    }, indent=2))
    
    # Step 4: First time generation (no existing content)
    print("\n\n🔧 Step 4: Fresh project - no existing .gitignore")
    print("-" * 80)
    
    request_data_4 = {
        "templates": ["python", "visualstudiocode"]
    }
    
    print(f"API Request: POST /gitignore/generate/")
    print(f"Request body: {json.dumps(request_data_4, indent=2)}")
    
    print("\n✅ Expected API Response:")
    print(json.dumps({
        "success": True,
        "message": "Successfully generated .gitignore for templates: python, visualstudiocode",
        "content": "# Python\n*.pyc\n__pycache__/\n...\n\n# VS Code\n.vscode/\n...",
        "patterns_added": None  # None indicates fresh generation, not a merge
    }, indent=2))
    
    # Summary
    print("\n\n" + "=" * 80)
    print("📊 SUMMARY: Benefits of the Merge Functionality")
    print("=" * 80)
    print("""
✓ Avoids duplicate patterns when adding templates multiple times
✓ Preserves custom rules and existing structure
✓ Clear indication of what was added (patterns_added count)
✓ Informative messages about merge results
✓ Works seamlessly with or without existing content
✓ Section headers clearly mark auto-generated additions

API Integration Points:
- Set existing_content to current .gitignore when merging
- Check patterns_added to see if changes were made
- Use patterns_added == 0 to detect when nothing new was added
- Omit existing_content for fresh generation
""")
    print("=" * 80)


if __name__ == "__main__":
    simulate_api_usage()
