---
name: handoff-continue
description: Use when starting work on a repo that has a HANDOFF.md or HANDOFF.local.md and the previous session's context must be recovered
---

Read `HANDOFF.local.md` first if it exists, then `HANDOFF.md`. Read both — neither is a summary of the other.

Each is authoritative over its own domain:

- **`HANDOFF.local.md` — the active front.** Once this file exists, your next task comes from here.
- **`HANDOFF.md` — shared facts:** pools, live resources and their owner, backlog, gotchas. These constrain the work; they do not select it.

A `HANDOFF.md` that declares an in-progress task is describing someone else's front once `HANDOFF.local.md` exists. Taking it means colliding with a teammate mid-task.

Identify the next task. State which file it came from.

Recommend the best-fit model — a recommendation for your human partner, not a switch you perform.

Suggest the `mcp` command with the appropriate servers from `mcp --list`, one `--add` per line. Recommend none when none fit; do not pad the list.

On the repository's base branch — `main`, `master`, or whatever the trunk is here — create and switch to a branch named for the task being resumed.

Finished a task from a handoff? Remove it from the file that holds it and append it to that same file's completed-work section, creating one at the bottom if absent. Do not invent a separate doc.
