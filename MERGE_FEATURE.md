# Merging .gitignore Files - Feature Documentation

## Overview

The gitignore MCP tool now supports intelligent merging of .gitignore patterns, preventing duplicate entries and maintaining file structure when adding new templates.

## How It Works

### Without Merge (Previous Behavior)
When you request templates without existing content, you get the full template:

```json
POST /gitignore/generate/
{
  "templates": ["python"]
}

Response:
{
  "success": true,
  "message": "Successfully generated .gitignore for templates: python",
  "content": "# Full Python template content...",
  "patterns_added": null
}
```

### With Merge (New Feature)
When you provide existing .gitignore content, only new patterns are added:

```json
POST /gitignore/generate/
{
  "templates": ["python"],
  "existing_content": "# My custom rules\n*.log\ntmp/\n"
}

Response:
{
  "success": true,
  "message": "Added 42 new pattern(s) from templates: python",
  "content": "# My custom rules\n*.log\ntmp/\n\n# === Patterns added by mcp-gitignore ===\n*.pyc\n__pycache__/\n...",
  "patterns_added": 42
}
```

## Key Features

### 1. Smart Deduplication
- Compares patterns while ignoring comments and empty lines
- Only adds patterns that don't already exist
- Case-sensitive pattern matching

### 2. Structure Preservation
- Keeps existing comments and formatting
- Preserves custom rules and organization
- Adds new patterns under a clear section header

### 3. No-Change Detection
When all patterns already exist:
```json
{
  "success": true,
  "message": "No new patterns to add. All patterns from templates (python) already exist.",
  "content": "# Original content unchanged",
  "patterns_added": 0
}
```

### 4. Clear Section Markers
New patterns are added under a distinctive header:
```
# === Patterns added by mcp-gitignore ===
pattern1
pattern2
pattern3
```

## API Changes

### GitignoreGenerateRequest
```python
{
  "templates": ["python", "node"],        # Required: list of template names
  "existing_content": "..."               # Optional: existing .gitignore content
}
```

### GitignoreGenerateResponse
```python
{
  "success": true,                        # Operation status
  "message": "...",                       # Human-readable message
  "content": "...",                       # Merged/generated content
  "patterns_added": 42                    # Count of new patterns (null if not merging)
}
```

## Usage Examples

### Example 1: Starting Fresh
```python
# First time - no existing content
request = {"templates": ["python"]}
# Result: Full Python template
```

### Example 2: Adding to Existing File
```python
# Already have some patterns
existing = "*.log\ntemp/\n"
request = {"templates": ["python"], "existing_content": existing}
# Result: Existing patterns + new Python patterns
```

### Example 3: Avoiding Duplicates
```python
# Already have Python patterns
existing = "*.pyc\n__pycache__/\n..."
request = {"templates": ["python"], "existing_content": existing}
# Result: No changes (patterns_added: 0)
```

### Example 4: Multi-Language Project
```python
# Python project adding Node.js
existing = "# Python\n*.pyc\n__pycache__/\n"
request = {"templates": ["node"], "existing_content": existing}
# Result: Python patterns + Node.js patterns
```

## Benefits

✅ **No Duplicates**: Patterns are never added twice  
✅ **Clean Files**: Maintains readable, organized .gitignore files  
✅ **Custom Rules**: Preserves hand-written patterns and comments  
✅ **Visibility**: Clear indication of what was added and when  
✅ **Efficiency**: Skips merge if no new patterns exist  
✅ **Backwards Compatible**: Works with or without existing content  

## Testing

The merge functionality is thoroughly tested:
- 12 unit tests for merge logic
- 8 integration tests for API endpoints
- Real-world scenario testing
- Security scanning (0 vulnerabilities)

## Implementation Details

The merge algorithm:
1. Parses existing content, extracting non-comment, non-empty patterns
2. Parses template content similarly
3. Identifies patterns in template not in existing
4. Returns unchanged content if no new patterns
5. Otherwise, appends new patterns under section header

Pattern comparison:
- Strips leading/trailing whitespace
- Ignores lines starting with `#` (comments)
- Ignores empty lines
- Case-sensitive matching
- Preserves original pattern formatting
