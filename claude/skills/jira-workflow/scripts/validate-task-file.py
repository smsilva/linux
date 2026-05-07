#!/usr/bin/env python3
"""
PreToolUse hook — validates Jira task files before Write.
Denies writes to */.jira/*.md (except config.md) that don't
match the required template format.
"""
import json, re, sys

data = json.load(sys.stdin)

if data.get("hook_event_name") != "PreToolUse":
    sys.exit(0)
if data.get("tool_name") != "Write":
    sys.exit(0)

tool_input = data.get("tool_input", {})
file_path = tool_input.get("file_path", "")
content = tool_input.get("content", "")

# Only validate jira task files (not config.md)
import os
if not (("/.jira/" in file_path or file_path.startswith(".jira/"))
        and file_path.endswith(".md")
        and not file_path.endswith("config.md")):
    sys.exit(0)

errors = []

lines = content.splitlines()
first_line = lines[0] if lines else ""

if not re.match(r"^# [A-Z]+-\d+: .+", first_line):
    errors.append(
        f"Line 1 must be '# ISSUE_KEY: Summary' — got: {first_line!r}\n"
        "  (use colon ':', not em dash '—'; no YAML frontmatter)"
    )

if "**Task:**" not in content:
    errors.append("Missing '**Task:**' field with URL link")

if "**Owner:**" not in content:
    errors.append("Missing '**Owner:**' field (not **Assignee:** or **Responsável:**)")

if "\n## Description\n" not in content and not content.startswith("## Description\n"):
    errors.append(
        "Missing '## Description' section\n"
        "  (not ## Descrição, ## Objetivo, ## Descripción, or any translation)"
    )

if "\n## Work log\n" not in content:
    errors.append("Missing '## Work log' section with 5 ### subsections")

if errors:
    reason = (
        f"Jira task file format is wrong ({file_path}):\n"
        + "\n".join(f"  - {e}" for e in errors)
        + "\n\nDo NOT use the Write tool for task files. "
        "Use create-task-file.py:\n"
        "  1. Write issue description to /tmp/jira_description.txt\n"
        "  2. Run: python3 ~/.claude/skills/jira-workflow/scripts/create-task-file.py --template ~/.claude/skills/jira-workflow/templates/task.md --output ..."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)

sys.exit(0)
