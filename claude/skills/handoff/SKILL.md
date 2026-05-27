---
name: handoff
description: Use when ending a session or completing a milestone to create or update HANDOFF.md so the next agent can continue without context loss
---

Capture only what exists in the conversation. Skip anything reproducible from git.

The HANDOFF.md is read by another agent. Write it imperatively and densely, no narration or context-setting.

1. Invoke the `save-session-learnings` skill.

2. Read `HANDOFF.md` if it exists.

3. Write `HANDOFF.md` at the project root with these sections:
   - **Why**: problem being solved, approach chosen, alternatives rejected.
   - **In Progress**: last step taken and intended next step at the moment of stopping.
   - **Open Questions / Hypotheses**: unresolved investigations and unconfirmed suspicions.
   - **Known Broken**: each item marked *intentional* or *unexpected*.
   - **How to Resume**: a concrete first command.
   - **Next Steps**: concrete action items. Omit git workflow (commits, PRs, merges).

4. Append this line at the end of the file, verbatim:
   > Before trusting anything time-sensitive above, run `git status`, `git diff`, and `git log` against the base branch.
