---
name: fan-out
description: Use before fanning work out to parallel subagents, for bulk mechanical file work (porting, translating, expanding a table into one file per row) or one subagent per issue.
---

# fan-out

## Bulk mechanical file work

Fan out to Sonnet subagents in parallel, one batch of ~8–14 files each, up to 5–6 at a time. Give every batch the same rule block plus its explicit file list, and tell each agent to report only a one-line confirmation and anomalies — never file contents. Verify centrally afterwards (forbidden tokens, link resolution, orphan files) rather than trusting the reports.

Batches that share one worktree never run `git stash`, `git checkout -- <path>`, `git reset` or `git rebase` (owner, 2026-11-25, Nereus #2242: two batches ran `git stash` while three edited one worktree, and the `pop` failed on another batch's change): to compare with the original, read `git show HEAD:<file>` instead.

## Parallel subagents, one issue each

Owner, 2026-11-12, platform-api FLWP-75938..75942:

- Give each its own scratch directory (`<scratchpad>/<issue>/`), since five sharing one scratchpad overwrote each other's commit-message file.
- Ask each to run only the checks its change touches (its own tests, the hooks it wires, lint, docs build), leaving the full suite to CI: five full test suites at once were slow and hit Docker timeouts.
