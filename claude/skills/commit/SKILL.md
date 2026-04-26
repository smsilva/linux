---
name: commit
description: Commits all pending changes in the working tree
---

Dispatch the `judite-developer` agent via the Agent tool (`model: "haiku"`) to perform the commit. Pass the current working directory and these rules to the agent:

- Do not amend existing commits
- NEVER commit on the `main` branch — if on `main`, suggest a branch name, create it, push, then commit there
- If not on `main`: commit and push
- Different commits for different changes context
- Follow conventional commits format (`type(scope): description`)