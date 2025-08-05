from fastapi import FastAPI, HTTPException
from fastmcp import FastMCP
import httpx
import os
from typing import List
from mcp_tools.schemas import (
    GitignoreGenerateRequest,
    GitignoreGenerateResponse,
    GitignoreListResponse,
)

app = FastAPI(
    title="Gitignore MCP Tool",
    description="A MCP-compliant FastAPI service for generating .gitignore files using gitignore.io API.",
    version="0.1.0",
)

GITIGNORE_API_BASE = "https://www.toptal.com/developers/gitignore/api"


@app.get(
    "/gitignore/templates/",
    operation_id="list_gitignore_templates",
    response_model=GitignoreListResponse,
)
async def list_gitignore_templates():
    """List all available gitignore templates from gitignore.io"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{GITIGNORE_API_BASE}/list?format=lines")
            response.raise_for_status()

            # Parse the response - it's a comma-separated list
            templates = [t.strip() for t in response.text.strip().split(",")]
            return GitignoreListResponse(templates=templates)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch templates: {str(e)}"
        )


@app.post(
    "/gitignore/generate/",
    operation_id="generate_gitignore",
    response_model=GitignoreGenerateResponse,
)
async def generate_gitignore(request: GitignoreGenerateRequest):
    """Generate a .gitignore file based on specified templates and save it to the specified path"""
    try:
        # Join templates with commas for the API call
        templates_str = ",".join(request.templates)

        # Fetch gitignore content from gitignore.io
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{GITIGNORE_API_BASE}/{templates_str}")
            response.raise_for_status()

            gitignore_content = response.text

        # Write to file
        os.makedirs(
            os.path.dirname(request.output_path)
            if os.path.dirname(request.output_path)
            else ".",
            exist_ok=True,
        )

        with open(request.output_path, "w", encoding="utf-8") as f:
            f.write(gitignore_content)

        return GitignoreGenerateResponse(
            success=True,
            message=f"Successfully generated .gitignore for templates: {', '.join(request.templates)}",
            content=gitignore_content,
            file_path=os.path.abspath(request.output_path),
        )

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=400,
                detail=f"One or more templates not found. Available templates can be retrieved from /gitignore/templates/",
            )
        raise HTTPException(status_code=500, detail=f"API error: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate .gitignore: {str(e)}"
        )


mcp = FastMCP.from_fastapi(app=app)

if __name__ == "__main__":
    mcp.run()
