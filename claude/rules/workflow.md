# Workflow

- Walk Skeleton is always preferred approach for development: ship a thin end-to-end slice early for feedback
- `CLAUDE.local.md` deve estar sempre no `.gitignore` de qualquer repositório (arquivo local, não versionado, análogo a `HANDOFF.local.md`)
- PRs (Bitbucket and GitHub): detect the host via `git remote get-url origin`.
  - Generate a description and save it as `/tmp/<branch>-pr.txt` using markdown
  - In chat messages: show absolute file paths so the user can click/open in the editor
  - In the PR description: use repo-relative paths only (no local `/home/<user>/...` prefix)
  - **GitHub** (`github.com`): open via `gh pr create`; if it fails, show the URL `https://github.com/<org>/<repo>/compare/<branch>?expand=1`
  - **Bitbucket** (`bitbucket.org`): show the URL `https://bitbucket.org/.../pull-requests/new?source=<branch>&t=1`
- Bulk mechanical file work (porting, translating, expanding a table into one file per row): fan out to Sonnet subagents in parallel, one batch of ~8–14 files each, up to 5–6 at a time. Give every batch the same rule block plus its explicit file list, and tell each agent to report only a one-line confirmation and anomalies — never file contents. Verify centrally afterwards (forbidden tokens, link resolution, orphan files) rather than trusting the reports.
- Keep feature PRs focused on the topic in the branch name. When `HANDOFF.md`, status reports, or other cross-cutting docs accumulate on a `feat/*` branch, split them into a sister `chore/<same-id>-docs-handoff` branch from `main`, merge it first, then `git reset --hard origin/main` + cherry-pick the topical commits onto the feature branch and force-push. Create a `backup/<branch>-pre-cleanup` ref before destructive resets — the harness may block `--hard` against the feature branch otherwise.
