---
name: handoff
description: Use when ending a session, completing a milestone, or stopping mid-task and context must be preserved in HANDOFF.md for the next agent
---

Capture only what exists in the conversation. Skip anything reproducible from git unless it was explicitly requested.

The handoff will be read by another agent. Write it imperatively and densely, no narration or context-setting.

Never mention git commits, PRs, or merges in the handoff text.

## Two files, or one

`HANDOFF.local.md` exists, or the project's instructions define the split → write both. Otherwise `HANDOFF.md` alone.

Route each fact by asking **"is this true no matter who is working, or does it describe my machine?"** — not "is this important?"

| `HANDOFF.md` — shared, versioned | `HANDOFF.local.md` — personal, gitignored |
|---|---|
| Facts about the account, project or repo: pools others draw from, live resources and their owner, backlog, gotchas about code or third-party behaviour, work already delivered | Active front — why, last step, intended next step; state of my local environment — what runs, what is applied, what I own; host-specific quirks |

"The cluster is up" or "the environment is ready" describes one machine, not the project. It goes in the local file.

## Steps

1. **REQUIRED:** Invoke the `save-session-learnings` skill.

2. Read `HANDOFF.local.md` first if it exists, then `HANDOFF.md`. Carry still-relevant Open Questions and Known Broken items forward into the file you are writing.

3. Write these sections — into `HANDOFF.local.md` when the split applies, otherwise into `HANDOFF.md`:
   - **Why**: problem being solved, approach chosen, alternatives rejected.
   - **In Progress**: last step taken and intended next step at the moment of stopping.
   - **Open Questions / Hypotheses**: unresolved investigations and unconfirmed suspicions.
   - **Known Broken**: each item marked *intentional* or *unexpected*.
   - **How to Resume**: a concrete first command.
   - **Next Steps**: concrete action items.

4. Writing `HANDOFF.local.md`? Add it to `.gitignore` if missing, before any `git add`. That entry is also what tells the next reader the file is personal rather than a second workstream, so add it even when the file is nearly empty.

5. With the split, edit `HANDOFF.md` in place — never rewrite it whole. Leave entries you did not write where they are, including ones that look misfiled: "my machine" in a shared file is not attributable, and moving another person's note out of that file loses it for them. Refiling what is already there is your human partner's call. Without the split, writing `HANDOFF.md` whole is fine.

6. Ensure this line is the last line of every handoff file you wrote, verbatim:
   > Before trusting anything time-sensitive above, run `git status`, `git diff`, and `git log` against the base branch.

7. Finish by telling your human partner the handoff is written and they can safely run `/clear`.
