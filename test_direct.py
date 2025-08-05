#!/usr/bin/env python3
"""
Direct test of the gitignore functionality without running the full MCP server
"""

import asyncio
import httpx
import os


async def test_direct_gitignore():
    """Test the gitignore.io API directly"""

    print("🚀 Testing gitignore.io API directly...")

    GITIGNORE_API_BASE = "https://www.toptal.com/developers/gitignore/api"

    async with httpx.AsyncClient() as client:
        # Test 1: List templates
        print("\n🔍 Fetching available templates...")
        try:
            response = await client.get(f"{GITIGNORE_API_BASE}/list?format=lines")
            response.raise_for_status()
            templates = [t.strip() for t in response.text.strip().split(",")]
            print(f"✅ Found {len(templates)} templates")
            print(f"📝 Sample templates: {templates[:10]}")
        except Exception as e:
            print(f"❌ Error fetching templates: {e}")
            return

        # Test 2: Generate .gitignore for common development setup
        print("\n🔧 Generating .gitignore for Python + VSCode + macOS...")
        try:
            templates_to_use = ["python", "visualstudiocode", "macos"]
            templates_str = ",".join(templates_to_use)

            response = await client.get(f"{GITIGNORE_API_BASE}/{templates_str}")
            response.raise_for_status()

            gitignore_content = response.text

            # Save to file
            output_path = "example.gitignore"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(gitignore_content)

            print(f"✅ Successfully generated .gitignore")
            print(f"📁 Saved to: {os.path.abspath(output_path)}")
            print(f"📊 Content size: {len(gitignore_content)} characters")
            print(f"\n📝 First 300 characters:")
            print("-" * 50)
            print(gitignore_content[:300])
            if len(gitignore_content) > 300:
                print("...")
            print("-" * 50)

        except Exception as e:
            print(f"❌ Error generating .gitignore: {e}")


if __name__ == "__main__":
    asyncio.run(test_direct_gitignore())
