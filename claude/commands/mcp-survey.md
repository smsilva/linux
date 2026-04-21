Survey available MCP servers from a given repository URL and recommend which ones to add to the current project.

Usage: /mcp-survey <url>
Example: /mcp-survey https://github.com/awslabs/mcp/tree/main

The argument $ARGUMENTS is the URL of the MCP server registry to survey. If no URL is provided, try to discover at https://code.claude.com/docs/en/mcp

Steps:
1. Fetch $ARGUMENTS (or the default URL) and list all available MCP server packages
2. Check prerequisites: run `which uv uvx python3 2>&1; uv --version 2>&1; uvx --version 2>&1; python3 --version 2>&1`
3. Read the current project's .mcp.catalog.json (or ~/.claude/mcp.catalog.json if no project file) to identify already-configured servers
4. If no local catalog is found, ask the user if they want to create one from the global catalog
5. If the global catalog not existed too, create only the local catalog with an empty list of servers and proceed with the survey
6. If the mcp is present on the global catalog but not the local one, ask the user if they want to add it to the local catalog and proceed based on their response
7. Analyze the current project context (CLAUDE.md, scripts, services, infrastructure) to understand what AWS services are actively used
8. Cross-reference available servers against active services — exclude already-configured ones
9. Present a prioritized table: server name | reason relevant | safe flags (e.g. --readonly)
10. Ask the user which servers to add
11. For each selected server, fetch its README to get exact package name and required env vars, then add the entry to .mcp.catalog.json using uvx with FASTMCP_LOG_LEVEL=ERROR and appropriate flags

Prerequisites check: if uv/uvx are missing, instruct the user to run `curl -LsSf https://astral.sh/uv/install.sh | sh` before proceeding.
