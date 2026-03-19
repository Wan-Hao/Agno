# Qdrant Docs MCP Configuration Guide

This guide explains how to configure the Qdrant documentation MCP server for use with Qoder IDE in the Agno project.

## What is Qdrant Docs MCP?

The Qdrant docs MCP (Model Context Protocol) server provides LLMs with access to the latest and most accurate Qdrant documentation. This is a read-only MCP server that allows AI assistants to retrieve documentation and code snippets for Qdrant.

**Repository**: https://github.com/qdrant/mcp-for-docs

## Prerequisites

1. **uv package manager** - Required to run the Qdrant docs MCP server
   ```bash
   # Install uv if not already installed
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Qoder IDE** - Version 0.2.10 or later

## Installation Steps

### Step 1: Install uv (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation, restart your terminal or source your shell configuration:
```bash
source ~/.zshrc  # or ~/.bashrc depending on your shell
```

### Step 2: Install Qdrant Docs MCP Server

The server will be automatically installed when you first use it through `uvx`. No manual installation is required.

### Step 3: Configure MCP in Qoder IDE

1. **Open Qoder Settings**:
   - Click the user icon in the upper-right corner of Qoder IDE, OR
   - Use keyboard shortcut: `⌘⇧,` (macOS) or `Ctrl+Shift+,` (Windows)
   - Select **Qoder Settings**

2. **Navigate to MCP Settings**:
   - In the left-side navigation pane, click **MCP**

3. **Add Qdrant Docs MCP Server**:
   - On the **My Servers** tab, click **+ Add** in the upper-right corner
   - In the JSON editor that appears, add the following configuration:

```json
{
  "mcpServers": {
    "qdrant-docs": {
      "command": "uvx",
      "args": [
        "qdrant-mcp-for-docs"
      ],
      "env": {}
    }
  }
}
```

4. **Save Configuration**:
   - Close the file and click **Save** when prompted
   - The link icon (🔗) should appear next to the server name, indicating a successful connection
   - Expand the entry to view the available tools

## Available Tools

Once configured, the Qdrant docs MCP server provides tools for:

- **Retrieving Qdrant documentation**: Access the latest documentation for Qdrant features
- **Finding code snippets**: Get relevant code examples from Qdrant docs
- **Searching documentation**: Query specific topics within Qdrant documentation

## Usage Examples

### Example 1: Query Qdrant Documentation

In Qoder IDE's Agent mode, you can ask:

```
How do I create a collection in Qdrant?
```

The agent will use the Qdrant docs MCP server to retrieve the latest documentation and provide accurate guidance.

### Example 2: Find Code Examples

```
Show me an example of indexing vectors in Qdrant with Python
```

The MCP server will fetch relevant code snippets from the official documentation.

### Example 3: Learn About Qdrant Features

```
What are the different distance metrics available in Qdrant?
```

The agent will retrieve documentation about Qdrant's distance metrics and explain them.

## Verification

To verify the MCP server is working correctly:

1. Go to **Qoder Settings** → **MCP** → **My Servers**
2. Look for the **qdrant-docs** entry
3. Check that the link icon (🔗) is displayed (indicates successful connection)
4. Expand the server entry to see the list of available tools

## Troubleshooting

### Server fails to start

**Issue**: The MCP server doesn't connect (no link icon)

**Solution**:
1. Verify `uv` is installed correctly:
   ```bash
   uv --version
   ```
2. Try installing the package manually:
   ```bash
   uvx qdrant-mcp-for-docs
   ```
3. Check Qoder IDE logs for error messages

### Command not found: uvx

**Issue**: System cannot find the `uvx` command

**Solution**:
1. Ensure `uv` is installed:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. Add `uv` to your PATH (usually automatically done by the installer)
3. Restart your terminal/IDE

### No tools available

**Issue**: Server connects but no tools are shown

**Solution**:
1. Restart Qoder IDE
2. Remove and re-add the MCP server configuration
3. Check the Qdrant MCP server repository for updates

## Integration with Agno Project

The Qdrant docs MCP server can be particularly useful for the Agno project when:

- **Building knowledge graphs**: Understanding Qdrant's vector database capabilities for storing educational content
- **Implementing semantic search**: Using Qdrant for semantic similarity searches in educational materials
- **Optimizing retrieval**: Learning about Qdrant's indexing and query optimization features

## References

- [Qdrant MCP for Docs Repository](https://github.com/qdrant/mcp-for-docs)
- [Qoder MCP Documentation](https://docs.qoder.com/user-guide/chat/model-context-protocol)
- [Model Context Protocol](https://modelcontextprotocol.io/introduction)
- [uv Package Manager](https://github.com/astral-sh/uv)

## Notes

- This is a **read-only** MCP server - it only retrieves documentation, doesn't modify anything
- The server provides access to **curated and up-to-date** Qdrant documentation
- No API keys or tokens are required for this MCP server
- Maximum of 10 MCP servers can be used simultaneously in Qoder IDE
- MCP servers only work in **Agent mode** in Qoder IDE
