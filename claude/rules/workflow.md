# Workflow

- Walk Skeleton is always preferred approach for development: ship a thin end-to-end slice early for feedback
- `CLAUDE.local.md` deve estar sempre no `.gitignore` de qualquer repositório (arquivo local, não versionado, análogo a `HANDOFF.local.md`)
- Commit only on a branch, never on `main` (or the repository's trunk): if on it, create a branch named for the change first, then commit there. Every change reaches `main` through a PR.
- Worktrees (the owner's repositories): a session may have its home in the main clone (one per tmux window), but every change goes into its own worktree; the main clone is only read and pulled. `claude-guard-main-clone` (a `PreToolUse` hook) refuses commits and file edits in a main clone, except files git ignores; use the repository's own helper (`scripts/worktree/new` in Nereus) or `git worktree add ../<repo>-<slug> -b <type>/<slug> origin/main`.
- PRs (Bitbucket and GitHub): detect the host via `git remote get-url origin`.
  - Generate a description and save it as `/tmp/<branch>-pr.txt` using markdown
  - In chat messages: show absolute file paths so the user can click/open in the editor
  - In the PR description: use repo-relative paths only (no local `/home/<user>/...` prefix)
  - **GitHub** (`github.com`): open via `gh pr create`; if it fails, show the URL `https://github.com/<org>/<repo>/compare/<branch>?expand=1`
  - **Bitbucket** (`bitbucket.org`): show the URL `https://bitbucket.org/.../pull-requests/new?source=<branch>&t=1`
- Merging PRs: rebase merge (`gh pr merge --rebase --delete-branch`), never a merge commit. Before merging, reorganize the branch's commits into one commit per topic, each a Conventional Commit; force-push the reorganized branch, then merge.
- Bulk mechanical file work (porting, translating, expanding a table into one file per row): fan out to Sonnet subagents in parallel, one batch of ~8–14 files each, up to 5–6 at a time. Give every batch the same rule block plus its explicit file list, and tell each agent to report only a one-line confirmation and anomalies — never file contents. Verify centrally afterwards (forbidden tokens, link resolution, orphan files) rather than trusting the reports.
- Keep feature PRs focused on the topic in the branch name. When `HANDOFF.md`, status reports, or other cross-cutting docs accumulate on a `feat/*` branch, split them into a sister `chore/<same-id>-docs-handoff` branch from `main`, merge it first, then `git reset --hard origin/main` + cherry-pick the topical commits onto the feature branch and force-push. Create a `backup/<branch>-pre-cleanup` ref before destructive resets — the harness may block `--hard` against the feature branch otherwise.
- After a PR merges, and when asked about local leftovers, clean up the local clone: remove the merged branch's worktree, delete local branches whose upstream is `[gone]` and whose content is already on `main` (check with `git cherry origin/main <branch>` or the PR state, since rebase merges rewrite SHAs), and delete the `backup/*` refs created for that branch. Never delete a branch or worktree with uncommitted changes or work not on any remote.
