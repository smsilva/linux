Commits all pending changes in the working tree.

## Steps

1. **Identify files to commit**

- run `git status` and `git diff --stat` to see all modified files

2. Group files by logical concern. Each group becomes one commit.

3. For each group:
   - Use the `conventional-commits` skill to determine the commit message
   - `git add <files>`
   - `git commit -m "<message>"`

4. Run `git status` at the end to confirm.

5. If not in the `main` branch, push commits to the remote repository if needed: `git push origin <branch-name>` 

## Constraints

- Do not use `git add -A` or `git add .` — always add files explicitly by name
- Do not amend existing commits
