#!/usr/bin/env python3
"""
PreToolUse hook — validates Jira task files before Write.
Denies writes to */<JIRA_FOLDER>/*.md (except config.md) that don't
match the required template format.

Usage: python3 validate-task-file.py <JIRA_FOLDER>
  argv[1]: Jira folder path (e.g. ".jira") — used only to filter which
           Write calls to validate. The actual file path and content come
           from stdin as a JSON payload, e.g.:
             {
               "hook_event_name": "PreToolUse",
               "tool_name": "Write",
               "tool_input": {
                 "file_path": ".jira/PROJ-123.md",
                 "content": "..."
               }
             }
"""
import json, os, re, sys

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CREATE_SCRIPT = os.path.join(SCRIPT_DIR, 'create-task-file.py')
JIRA_FOLDER = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else ".jira"

data = json.load(sys.stdin)

if data.get("hook_event_name") != "PreToolUse":
    sys.exit(0)
if data.get("tool_name") != "Write":
    sys.exit(0)

tool_input = data.get("tool_input", {})
file_path = tool_input.get("file_path", "")
content = tool_input.get("content", "")

# Only validate jira task files (not config.md)
is_jira_file = (
    (("/" + JIRA_FOLDER + "/") in file_path or file_path.startswith(JIRA_FOLDER + "/"))
    and file_path.endswith(".md")
    and not file_path.endswith("config.md")
)
if not is_jira_file:
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
        "  1. Write issue description to /tmp/jira_description_<ISSUE_KEY>.txt\n"
        f"  2. Run: python3 {CREATE_SCRIPT} --output ..."
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
