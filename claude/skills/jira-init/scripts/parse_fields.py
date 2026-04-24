#!/usr/bin/env python3
"""Parse getJiraIssueTypeMetaWithFields MCP tool output and print field summary."""
import json, sys

path = sys.argv[1]
with open(path) as f:
    outer = json.load(f)

text = outer[0]["text"]
data = json.loads(text)
fields = data.get("fields", [])

for field in fields:
    req = "REQUIRED" if field.get("required") else "optional"
    fid = field.get("fieldId", "")
    name = field.get("name", "")
    av = field.get("allowedValues", [])
    av_str = ""
    if av:
        values = [v.get("value") or v.get("name", "") for v in av[:6]]
        av_str = f" | allowed: {values}" + (" ..." if len(av) > 6 else "")
    print(f"  {req:8} | {fid:25} | {name}{av_str}")
