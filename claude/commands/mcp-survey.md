Survey available MCP servers from a given repository URL and recommend which ones to add to the current project.

Usage: /mcp-survey <url>
Example: /mcp-survey https://github.com/awslabs/mcp/tree/main

The argument $ARGUMENTS is the URL of the MCP server registry to survey. If no URL is provided, default to https://github.com/awslabs/mcp/tree/main.

Steps:
1. Fetch $ARGUMENTS (or the default URL) and list all available MCP server packages
2. Check prerequisites: run `which uv uvx python3 2>&1; uv --version 2>&1; uvx --version 2>&1; python3 --version 2>&1`
3. Read the current project's .mcp.json (or ~/.claude/settings.json if no project file) to identify already-configured servers
4. Analyze the current project context (CLAUDE.md, scripts, services, infrastructure) to understand what AWS services are actively used
5. Cross-reference available servers against active services — exclude already-configured ones
6. Present a prioritized table: server name | reason relevant | safe flags (e.g. --readonly)
7. Ask the user which servers to add
8. For each selected server, fetch its README to get exact package name and required env vars, then add the entry to .mcp.json using uvx with FASTMCP_LOG_LEVEL=ERROR and appropriate flags

Prerequisites check: if uv/uvx are missing, instruct the user to run `curl -LsSf https://astral.sh/uv/install.sh | sh` before proceeding.
