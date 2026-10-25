---
name: ship
description: Commits pending changes, pushes, opens the PR and rebase-merges it into main ("commit push pr complete")
disable-model-invocation: true
---

Take the working tree all the way to `main` in one go. Stop and report on any failure — never force past a failing hook, check, or merge.

## Steps

1. **Commit** — follow the `commit` skill, with one exception: on a branch not yet merged, fold fixes to an existing commit into that commit (`git commit --amend` when it is `HEAD`, otherwise `git commit --fixup <sha>` + `GIT_SEQUENCE_EDITOR=: git rebase --interactive --autosquash main`).

2. **Organize** — `git log --oneline main..HEAD` must show one Conventional Commit per topic. Squash or split until it does.

3. **Push** — `git push --force-with-lease --set-upstream origin <branch>`.

4. **PR** — detect the host via `git remote get-url origin`.
   - Write the description to `/tmp/<branch>-pr.txt` (markdown, repo-relative paths, `## Summary` + `## Test plan`; tick only the checks you actually ran).
   - Reuse an open PR for the branch if one exists (`gh pr list --head <branch>`); otherwise `gh pr create --base main --head <branch> --title "<conventional title>" --body-file /tmp/<branch>-pr.txt`.
   - Bitbucket, or `gh pr create` failed: show the compare/new-PR URL and stop — merge is manual there.

5. **Merge** — `gh pr merge <number> --rebase --delete-branch`. Never a merge commit.

6. **Sync** — `git checkout main && git pull --ff-only`.

## Report

- PR number with its title, and the merged commits (`<sha> <subject>`)
- Absolute path of `/tmp/<branch>-pr.txt`
- What was verified and what was not (e.g. syntax check only, service not enabled)
