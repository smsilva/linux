# Workflow

- Walk Skeleton is always preferred approach for development: ship a thin end-to-end slice early for feedback
- Bitbucket PRs:
  - Show the Bitbucket URL for creation (`https://bitbucket.org/.../pull-requests/new?source=<branch>&t=1`)
  - In chat messages: show absolute file paths so the user can click/open in the editor
  - In the PR description: use repo-relative paths only (no local `/home/<user>/...` prefix)
  - Generate a description
  - Save it as `/tmp/<branch>-pr.txt` using markdown
- Keep feature PRs focused on the topic in the branch name. When `HANDOFF.md`, status reports, or other cross-cutting docs accumulate on a `feat/*` branch, split them into a sister `chore/<same-id>-docs-handoff` branch from `main`, merge it first, then `git reset --hard origin/main` + cherry-pick the topical commits onto the feature branch and force-push. Create a `backup/<branch>-pre-cleanup` ref before destructive resets — the harness may block `--hard` against the feature branch otherwise.
