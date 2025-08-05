<div align="center">

  <h1> Gitignore MCP Tool </h1>

</div>

> A MCP server for generating .gitignore files using gitignore.io API

## 🌟 Features

- **Gitignore Generation**: Generate .gitignore files for 600+ templates (languages, IDEs, OS)
- **Template Listing**: Browse all available gitignore templates

## 🛠️ Getting Started

### Environment Variables

| Variable             | Default                                           | Description                   |
| -------------------- | ------------------------------------------------- | ----------------------------- |
| `GITIGNORE_API_BASE` | `https://www.toptal.com/developers/gitignore/api` | Base URL for gitignore.io API |

### Local Development

- Install dependencies:

```bash
uv sync
```

- (Optional) Set custom API endpoint:
```bash
export GITIGNORE_API_BASE="https://your-custom-api.com/api"
```

- Run the MCP server:
```bash
uv run --with fastmcp fastmcp run mcp_tools/main.py
```

### Docker

- Build the Docker image:
```bash
docker build -t mcp-gitignore:latest .
```

- Run the container:
```bash
docker run -i --rm -p 8000:8000 mcp-gitignore:latest
```

- Run with custom API endpoint:
```bash
docker run -i --rm -p 8000:8000 -e GITIGNORE_API_BASE="https://your-custom-api.com/api" mcp-gitignore:latest
```

- Run MCP Server:

```json
{
  "mcpServers": {
    "mcp-gitignore": {
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
