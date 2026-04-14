Commit all pending changes in the current branch.

Steps:
1. Run `git status` and `git diff --stat` to see what is modified.
2. Run `git log --oneline -5` to understand the commit message style used in this repo.
3. Group the changed files by logical concern (e.g. feature, fix, docs, test). Each group becomes one commit.
4. For each group:
   - `git add <files>`
   - `git commit -m "<type>(<scope>): <description>"` following Conventional Commits
5. Run `git status` at the end to confirm the working tree is clean.

Do not use `git add -A` or `git add .` — always add files explicitly by name.
Do not amend existing commits.
