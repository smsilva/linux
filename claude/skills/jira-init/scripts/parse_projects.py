#!/usr/bin/env python3
"""Parse getVisibleJiraProjects MCP tool output and print project list."""
import json, sys

path = sys.argv[1]
with open(path) as f:
    outer = json.load(f)

text = outer[0]["text"]
data = json.loads(text)
projects = data.get("values", data) if isinstance(data, dict) else data

for p in sorted(projects, key=lambda x: x.get("key", "")):
    print(f"{p.get('key'):10} | {p.get('name'):50} | {p.get('projectTypeKey','')}")
