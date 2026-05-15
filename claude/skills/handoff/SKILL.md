---
name: handoff
description: Create or update a handoff document so the next agent with fresh context can continue the work
---

0. Invoke the `save-session-learnings` skill to persist any lasting knowledge from this session.

1. If `HANDOFF.md` exists, read it before proceeding.

2. Run `git log main..HEAD` to capture work since the last update.

3. Find open security issues: check `CLAUDE.md` for a "Security tracking" section with a custom path; otherwise use `docs/security/issues/*.md`. Exclude any `archived/` subfolder. For each file found, extract `id`, `severity`, and the one-line description.

4. If step 3 found files, open `HANDOFF.md` with an **⚠️ Open Security Issues** section listing each as `SEC-NNN (Severity) — title`, with a note to address them before new features.

5. Write `HANDOFF.md` in the project root with:
   - **Goal**: What we're trying to accomplish
   - **Current Progress**: What's been done so far
   - **What Worked**: Approaches that succeeded
   - **What Didn't Work**: Approaches that failed
   - **Next Steps**: Clear action items — if there are open security issues, list fixing them first
