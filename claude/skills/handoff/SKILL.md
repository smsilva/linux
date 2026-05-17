---
name: handoff
description: Create or update a handoff document so the next agent with fresh context can continue the work
---

0. Invoke the `save-session-learnings` skill to persist any lasting knowledge from this session.

1. If `HANDOFF.md` exists, read it before proceeding.

2. Run `git log main..HEAD` to capture work since the last update.

3. Find open security issues: check `CLAUDE.md` for a "Security tracking" section with a custom path; otherwise use `docs/security/issues/*.md`. Exclude any `archived/` subfolder. For each file found, extract `id`, `severity`, and the one-line description.

4. If `docs/specs/` exists, enumerate `docs/specs/*.md` (exclude `archived/`). For each file, extract the title (first `# ...` line) and the `**Status:**` value if present. Group by status — these are active or deferred specs.

5. If `docs/plans/` exists, enumerate `docs/plans/*.md` (exclude `archived/`). These are in-flight implementation plans — the next concrete step is to continue executing them.

6. If step 3 found files, open `HANDOFF.md` with an **⚠️ Open Security Issues** section listing each as `SEC-NNN (Severity) — title`, with a note to address them before new features.

7. Write `HANDOFF.md` in the project root with:
   - **Goal**: What we're trying to accomplish
   - **Current Progress**: What's been done so far
   - **What Worked**: Approaches that succeeded
   - **What Didn't Work**: Approaches that failed
   - **Next Steps**: Clear action items. Use steps 4–5 to populate:
     - In-flight plans (step 5) at the top — continue execution
     - `Approved` specs without a matching plan → "create a plan for X"
     - `Deferred` / other backlog specs → optional **Backlog** subsection
     - If there are open security issues, list fixing them first
