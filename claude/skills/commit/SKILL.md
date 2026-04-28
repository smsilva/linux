---
name: commit
description: Commits all pending changes in the working tree
---

- Run `git status` and `git diff` to understand what changed before staging
- Stage specific files by name — never `git add -A` or `git add .`
- If any file looks like a secret, env file, or build artifact, add it to `.gitignore` first
- Group related changes into one commit; separate unrelated changes into distinct commits
- Follow conventional commits format — use the `conventional-commits` skill
- Do not amend existing commits
- NEVER commit on `main`:
  - Suggest a branch name, create it, then commit there
- On any other branch: commit, then `git push` (add `--set-upstream origin <branch>` if no upstream is set)
