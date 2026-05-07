#!/usr/bin/env python3
import argparse, re, os, sys

parser = argparse.ArgumentParser(description="Create a Jira task file from template")
parser.add_argument("--template", required=True)
parser.add_argument("--output", required=True)
parser.add_argument("--issue-key", required=True)
parser.add_argument("--summary", required=True)
parser.add_argument("--site", required=True)
parser.add_argument("--story-key", default="")
parser.add_argument("--story-summary", default="")
parser.add_argument("--epic-key", default="")
parser.add_argument("--epic-summary", default="")
parser.add_argument("--status", required=True)
parser.add_argument("--assignee", required=True)
parser.add_argument("--sprint", default="")
parser.add_argument("--description-file", required=True)
args = parser.parse_args()

for path, label in [(args.template, "--template"), (args.description_file, "--description-file")]:
    if not os.path.exists(path):
        print(f"Error: {label} file not found: {path}", file=sys.stderr)
        sys.exit(1)

with open(args.template) as f:
    content = f.read()

with open(args.description_file) as f:
    description = f.read().strip()

values = {
    "{{ISSUE_KEY}}": args.issue_key,
    "{{SUMMARY}}": args.summary,
    "{{SITE}}": args.site,
    "{{STORY_KEY}}": args.story_key,
    "{{STORY_SUMMARY}}": args.story_summary,
    "{{EPIC_KEY}}": args.epic_key,
    "{{EPIC_SUMMARY}}": args.epic_summary,
    "{{STATUS}}": args.status,
    "{{ASSIGNEE}}": args.assignee,
    "{{SPRINT}}": args.sprint,
    "{{DESCRIPTION}}": description,
}

for placeholder, value in values.items():
    content = content.replace(placeholder, value)

if not args.story_key:
    content = re.sub(r"\n\*\*Story:\*\*[^\n]*", "", content)
if not args.epic_key:
    content = re.sub(r"\n\*\*Epic:\*\*[^\n]*", "", content)
if not args.sprint:
    content = re.sub(r"\n\*\*Sprint:\*\*[^\n]*", "", content)

os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
with open(args.output, "w") as f:
    f.write(content)

print(f"Created: {args.output}")
