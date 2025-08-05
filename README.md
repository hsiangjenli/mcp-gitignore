<div align="center">

  <h1> Gitignore MCP Tool </h1>

</div>

> A DevOps-friendly MCP server for generating .gitignore files using gitignore.io API with CI/CD, Docker, and Documentation-as-Code (DaC) support

## 🚀 Core Idea

This tool leverages **fastmcp** and **FastAPI** to seamlessly integrate MCP functionality for generating .gitignore files, while inheriting the original OpenAPI specifications.

## 🌟 Features

- **Gitignore Generation**: Generate .gitignore files for 600+ templates (languages, IDEs, OS)
- **Template Listing**: Browse all available gitignore templates
- **Environment Configuration**: Configurable API endpoint via environment variables
- **CI/CD Integration**: Automate your workflows with GitHub Actions
- **Dockerized Environment**: Consistent and portable development and production environments
- **Documentation-as-Code**: Automatically generate and deploy documentation using MkDocs
- **FastAPI Integration**: Build robust APIs with OpenAPI support

## 🛠️ Getting Started

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GITIGNORE_API_BASE` | `https://www.toptal.com/developers/gitignore/api` | Base URL for gitignore.io API |

### Local Development

1. Install dependencies:
   ```bash
   uv sync
   ```

2. (Optional) Set custom API endpoint:
   ```bash
   export GITIGNORE_API_BASE="https://your-custom-api.com/api"
   ```

3. Run the MCP server:
   ```bash
   uv run --with fastmcp fastmcp run mcp_tools/main.py
   ```

### Docker

1. Build the Docker image:
   ```bash
   docker build -t gitignore-mcp-tool:latest .
   ```

2. Run the container:
   ```bash
   docker run -i --rm -p 8000:8000 mcp-gitignore:latest
   ```

3. Run with custom API endpoint:
   ```bash
   docker run -i --rm -p 8000:8000 -e GITIGNORE_API_BASE="https://your-custom-api.com/api" mcp-gitignore:latest
   ```

4. Run MCP Server:
  ```json
  {
    "mcpServers": {
      "gitignore-mcp-tool": {
        "command": "docker",
        "args": [
          "run",
          "--rm",
          "-i",
          "-p",
          "8000:8000",
          "mcp-gitignore:latest"
        ],
        "env": {
          "GITIGNORE_API_BASE": "https://www.toptal.com/developers/gitignore/api"
        }
      }
    }
  }
  ```

## 🎯 API Endpoints

### List Templates
**GET** `/gitignore/templates/`

List all available gitignore templates.

### Generate .gitignore
**POST** `/gitignore/generate/`

Generate .gitignore file based on templates.

**Request Body:**
```json
{
  "templates": ["python", "visualstudiocode", "macos"],
  "output_path": ".gitignore"
}
```

## 📚 Documentation

- Documentation is built using MkDocs and deployed to GitHub Pages.
- To build the documentation locally:
  
  ```bash
  chmod +x scripts/build_docs.sh
  scripts/build_docs.sh
  mkdocs build
  ```
