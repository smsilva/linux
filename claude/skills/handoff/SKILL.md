---
name: handoff
description: Use when ending a session, completing a milestone, or stopping mid-task and context must be preserved for the next agent
---

Capture only what exists in the conversation. Skip anything reproducible from git unless it was explicitly requested.

The `HANDOFF.md` will be read by another agent. Write it imperatively and densely, no narration or context-setting.

Never mention git commits, PRs, merges.

1. Invoke the `save-session-learnings` skill.

2. Read `HANDOFF.md` if it exists. Extract still-relevant Open Questions and Known Broken items to carry forward.

3. Write `HANDOFF.md` at the project root with these sections:
   - **Why**: problem being solved, approach chosen, alternatives rejected.
   - **In Progress**: last step taken and intended next step at the moment of stopping.
   - **Open Questions / Hypotheses**: unresolved investigations and unconfirmed suspicions.
   - **Known Broken**: each item marked *intentional* or *unexpected*.
   - **How to Resume**: a concrete first command.
   - **Next Steps**: concrete action items.

4. Append this line at the end of the file, verbatim:
   > Before trusting anything time-sensitive above, run `git status`, `git diff`, and `git log` against the base branch.

5. Double-check to ensure a safety `/clear` invokation.
