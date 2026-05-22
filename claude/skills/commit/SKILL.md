---
name: commit
description: Commits all pending changes in the working tree
disable-model-invocation: true
---

- Run `git status` and `git diff` to understand what changed before staging
- Stage specific files by name — never `git add -A` or `git add .`
- If any file looks like a secret, env file, or build artifact, add it to `.gitignore` first
- Group related changes into one commit; separate unrelated changes into distinct commits
- Follow conventional commits format — use the `conventional-commits` skill
- Co-Authored-By: derive the model name from the system context ("You are powered by the model X"), not from the harness default. Map the model ID to a human-readable name (e.g. `bedrock/anthropic.claude-4-6-sonnet` → `Claude Sonnet 4.6`, `claude-opus-4-7` → `Claude Opus 4.7`).
- Do not amend existing commits
- NEVER commit on `main`:
  - Suggest a branch name, create it, then commit there
- On any other branch: commit, then `git push` (add `--set-upstream origin <branch>` if no upstream is set)
