List Claude Code sessions for a given date with their first prompt.

$ARGUMENTS may contain `--date YYYY-MM-DD` and/or `--project /path`. If no date is given, default to today (compute the actual date).

Steps:

1. Parse $ARGUMENTS for `--date` and `--project` (default project: current working directory).

2. Compute the sessions directory:
   - Encode the project path by replacing every non-alphanumeric character with `-`
   - Sessions dir: `~/.claude/projects/<encoded-path>/`

3. List all `.jsonl` files in that directory whose mtime matches the target date. Sort by mtime ascending.

4. For each session file, extract the first user message:
   - Parse lines as JSON; find the first object where `type == "user"`
   - Get `message.content` — it may be a string or a list of blocks
   - For list content, find the first block with `type == "text"`
   - Skip text that starts with `/` or `<` (slash commands and XML wrappers)
   - Truncate to 120 characters
   - If no valid message found, use "(slash command only)"

5. Present results as a markdown table with columns: UUID (first 8 chars), Time (HH:MM:SS), Topic.
