Survey available MCP servers from a given repository URL and recommend which ones to add to the catalog.

Usage: /mcp-survey <url>
Example: /mcp-survey https://github.com/awslabs/mcp/tree/main

$ARGUMENTS is the URL of the MCP server registry to survey. Required — no default fallback.

Steps:
1. Fetch $ARGUMENTS and list all available MCP server packages.
2. Check prerequisites: run `which uv uvx 2>&1; uv --version 2>&1; uvx --version 2>&1`
   - If uv/uvx are missing, tell the user to run `curl -LsSf https://astral.sh/uv/install.sh | sh` and stop.
3. Load state from disk:
   - Global catalog: ~/.claude/mcp.catalog.json — create `{"mcpServers": {}}` if missing.
   - Active servers: .mcp.json in current dir (written by mcp-select; may not exist).
   - Known = all keys in global catalog. Active = all keys in .mcp.json.
4. Analyze the current project context (CLAUDE.md, scripts, services, infrastructure) to identify technologies and services in active use.
5. For each server from the survey, classify it as one of:
   - **active**: already in .mcp.json — skip entirely.
   - **available**: in global catalog but not in .mcp.json — can be enabled with `mcp-select`, no catalog changes needed.
   - **new**: not in global catalog — needs to be fetched and added.
6. Present a table in two sections:
   - "Available (run mcp-select to enable)": name | reason relevant
   - "New — not yet in catalog": name | reason relevant | suggested safe flags (e.g. --readonly)
   Omit active servers. Sort each section by relevance to the project.
7. Ask the user which **new** servers to add. (Available ones need no action here.)
8. For each selected new server, fetch its README to get the exact package name and required env vars. Add to ~/.claude/mcp.catalog.json using this structure:
   ```json
   "server-name": {
     "command": "uvx",
     "args": ["--from", "package-name@latest", "server-command", "--any-safe-flags"],
     "env": { "FASTMCP_LOG_LEVEL": "ERROR" }
   }
   ```
   Include only env vars that are required; leave the value empty (`""`) for secrets the user must fill in.
9. After updating the catalog, remind the user to run `mcp-select` to activate servers in the current project.
