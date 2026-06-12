# Workflow

- Walk Skeleton is always preferred approach for development: ship a thin end-to-end slice early for feedback
- Bitbucket PRs:
  - Show the Bitbucket URL for creation (`https://bitbucket.org/.../pull-requests/new?source=<branch>&t=1`)
  - In chat messages: show absolute file paths so the user can click/open in the editor
  - In the PR description: use repo-relative paths only (no local `/home/<user>/...` prefix)
  - Generate a description
  - Save it as `/tmp/<branch>-pr.txt` using markdown
