# Workflow

- Walk Skeleton is always preferred approach for development: ship a thin end-to-end slice early for feedback
- `CLAUDE.local.md` is always in every repository's `.gitignore` (a local, unversioned file, like `HANDOFF.local.md`)
- Commit only on a branch, never on `main` (or the repository's trunk): if on it, create a branch named for the change first, then commit there. Every change reaches `main` through a PR.
- Worktrees (the owner's repositories): a session may have its home in the main clone (one per tmux window), but every change goes into its own worktree; the main clone is only read and pulled. `claude-guard-main-clone` (a `PreToolUse` hook) refuses commits and file edits in a main clone, except files git ignores; use the repository's own helper (`scripts/worktree/new` in Nereus) or `git worktree add ../<repo>-<slug> -b <type>/<slug> origin/main`.
- PRs (Bitbucket and GitHub): detect the host via `git remote get-url origin`; save the markdown description as `/tmp/<branch>-pr.txt`, with repo-relative paths only (absolute paths in chat). GitHub: `gh pr create`, falling back to `https://github.com/<org>/<repo>/compare/<branch>?expand=1`. Bitbucket: show `https://bitbucket.org/.../pull-requests/new?source=<branch>&t=1`.
- Merging PRs: rebase merge (`gh pr merge --rebase --delete-branch`), never a merge commit; first reorganize the branch into one Conventional Commit per topic and force-push it.
- Bulk mechanical file work and parallel subagents (one issue each): follow the `fan-out` skill. Branch hygiene and post-merge cleanup of the local clone: follow the `branch-cleanup` skill.
