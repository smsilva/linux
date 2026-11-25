---
name: branch-cleanup
description: Use after a PR merges or when the owner asks about local leftovers (worktrees, merged or gone branches, backup refs), and when cross-cutting docs (HANDOFF.md, status reports) pile up on a feature branch.
---

# branch-cleanup

## Keep feature PRs focused

Cross-cutting docs (`HANDOFF.md`, status reports) that pile up on a `feat/*` branch move to a sister `chore/<same-id>-docs-handoff` branch merged first; then rebuild the feature branch from `origin/main` with its topical commits, after a `backup/<branch>-pre-cleanup` ref.

## Clean up the local clone after a merge

- Remove the merged branch's worktree with `gwd`: it refuses while a tmux pane runs a program inside it and moves idle shells out. A session inside its own worktree runs `gwd --after-exit`, and the `SessionEnd` hook `gwd --hook` removes it once the session has exited. `claude-guard-worktree-remove` refuses a direct `git worktree remove`.
- Delete local branches whose upstream is `[gone]` and whose content is already on `main`: check with `git cherry origin/main <branch>` or the PR state, since rebase merges rewrite SHAs.
- Delete the `backup/*` refs created for that branch.
- Never delete a branch or worktree with uncommitted changes or work not on any remote.
