---
name: skill-review
description: Review a skill file for conciseness and clarity. Accepts a skill name (e.g. "handoff") or a full path to a SKILL.md file.
---

1. Resolve the skill file path:
   - If given a full path, use it directly.
   - If given a skill name, look in `~/.claude/skills/{name}/SKILL.md`.

2. Read the file.

3. Review for:
   - Redundant or mergeable steps
   - Vague instructions (prefer concrete commands over prose descriptions)
   - Implicit information that doesn't need to be stated
   - Awkward or overly verbose phrasing

4. Present a proposed revision with a brief list of changes made.

5. Ask the user to confirm before applying.
