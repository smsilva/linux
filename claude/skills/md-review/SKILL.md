---
name: md-review
description: Review a Markdown file for conciseness and clarity. Accepts a file path or a skill name (e.g. "handoff").
---

1. Resolve the file path:
   - If given a path ending in `.md` or containing `/`, use it directly.
   - If given a simple name (no `/`, no `.md`), look in `~/.claude/skills/{name}/SKILL.md`.

2. Read the file.

3. Open the file in VS Code: `code <resolved-path>`.

4. Review for:
   - Redundant or mergeable steps
   - Vague instructions (prefer concrete commands over prose descriptions)
   - Implicit information that doesn't need to be stated
   - Awkward or overly verbose phrasing

5. If issues found, list them and ask the user for approval before applying any changes via Edit.

6. If the file is in pt-br, translate it to English after reviewing.
