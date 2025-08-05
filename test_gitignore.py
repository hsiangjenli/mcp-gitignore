#!/usr/bin/env python3
"""
Test script to demonstrate the gitignore MCP functionality
"""

import asyncio
import httpx


async def test_gitignore_mcp():
    base_url = "http://localhost:8000"  # Adjust if running on different port

    async with httpx.AsyncClient() as client:
        # Test 1: List available templates
        print("🔍 Testing template listing...")
        try:
            response = await client.get(f"{base_url}/gitignore/templates/")
            if response.status_code == 200:
                templates = response.json()["templates"]
                print(f"✅ Found {len(templates)} templates")
                print(f"📝 First 10 templates: {templates[:10]}")
            else:
                print(f"❌ Failed to list templates: {response.status_code}")
        except Exception as e:
            print(f"❌ Error listing templates: {e}")

        # Test 2: Generate a .gitignore file
        print("\n🔧 Testing .gitignore generation...")
        try:
            request_data = {
                "templates": ["python", "visualstudiocode", "macos"],
                "output_path": "test.gitignore",
            }
            response = await client.post(
                f"{base_url}/gitignore/generate/", json=request_data
            )
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Successfully generated .gitignore")
                print(f"📁 Saved to: {result['file_path']}")
                print(f"📝 Content preview (first 200 chars):")
                print(result["content"][:200] + "...")
            else:
                print(f"❌ Failed to generate .gitignore: {response.status_code}")
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"❌ Error generating .gitignore: {e}")


if __name__ == "__main__":
    print("🚀 Testing Gitignore MCP Tool")
    print("Note: Make sure the MCP server is running on the expected port")
    asyncio.run(test_gitignore_mcp())
