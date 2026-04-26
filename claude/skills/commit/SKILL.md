---
name: commit
description: Commits all pending changes in the working tree
---

Dispatch a Haiku agent via the Agent tool (`model: "haiku"`) to perform the commit. Pass the current working directory and these rules to the agent:

- Do not amend existing commits
- NEVER commit on the `main` branch
- If in the `main` branch:
  - Give the user a branch name suggestion
  - Create a new branch
  - Push the new branch to the remote repository
  - Commit there
- If not in the `main` branch, push
- Different commits for different changes context