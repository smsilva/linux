Commit changes following Conventional Commits. Accepts an optional mode:

- **all** (default): commits all pending changes in the working tree
- **session**: commits only files modified in the last interaction of this session

## Steps

1. **Identify files to commit**
   - `all`: run `git status` and `git diff --stat` to see all modified files
   - `session`: review conversation history to identify files created or edited in the most recent exchange; run `git diff --stat <those files>` to confirm changes

2. Group files by logical concern. Each group becomes one commit.

3. For each group:
   - Use the `conventional-commits` skill to determine the commit message
   - `git add <files>`
   - `git commit -m "<message>"`

4. Run `git status` at the end to confirm.

## Constraints

- Do not use `git add -A` or `git add .` — always add files explicitly by name
- Do not amend existing commits
- `session` mode: do not include files modified in earlier interactions
