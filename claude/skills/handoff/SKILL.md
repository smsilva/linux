---
name: handoff
description: Use when ending a session or completing a milestone to create or update HANDOFF.md so the next agent can continue without context loss
---

1. Invoke the `save-session-learnings` skill.

2. Read `HANDOFF.md` if it exists.

3. Run `git log $(git symbolic-ref refs/remotes/origin/HEAD | sed 's|.*/||')..HEAD --oneline` to summarise work since the base branch.

4. Find open security issues: check `CLAUDE.md` for a "Security tracking" section with a custom path; otherwise use `docs/security/issues/*.md` (exclude `archived/`). Extract `id`, `severity`, and one-line description from each.

5. Enumerate active specs and plans: for each of `docs/specs/` and `docs/plans/` (or equivalent paths from `CLAUDE.md §7`), list `*.md` files excluding `archived/`. Extract the first `# ...` heading and `**Status:**` value from each.

6. Write `HANDOFF.md` in the project root with:
   - **Goal**: what the project is building
   - **Current State**: what's done and what's in-flight, informed by the git log (step 3)
   - **Open Security Issues** (if any from step 4): list as `SEC-NNN (Severity) — title`; note to fix before new features
   - **Active Specs / Plans** (if any from step 5): grouped by status; in-flight plans at the top of Next Steps
   - **Next Steps**: concrete action items — no git workflow steps (commits, PRs, merges belong to the user)
   - **Backlog**: deferred items
