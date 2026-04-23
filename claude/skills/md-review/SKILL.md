---
name: md-review
description: Review a Markdown file for conciseness and clarity. Accepts a file path or a skill name (e.g. "handoff").
---

1. Resolve the file path:
   - If given a path ending in `.md` or containing `/`, use it directly.
   - If given a simple name (no `/`, no `.md`), look in `~/.claude/skills/{name}/SKILL.md`.

2. Read the file.

3. Review for:
   - Redundant or mergeable steps
   - Vague instructions (prefer concrete commands over prose descriptions)
   - Implicit information that doesn't need to be stated
   - Awkward or overly verbose phrasing

4. Present a proposed revision with a brief list of changes made.

5. If the file is in pt-br, translate it to English after reviewing.
