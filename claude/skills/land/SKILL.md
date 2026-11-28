---
name: land
description: Commits pending changes, pushes, opens the PR and rebase-merges it into main ("commit push pr complete"); `/land end-to-end` (or "até o cluster") then delivers the merge to where it runs, building, releasing and deploying in a new tmux window; `/land push` sends one push notification when it ends
disable-model-invocation: true
---

Named `land`, not `ship`, since Claude Code's built-in `/ship` (commit, push and PR, never a merge) took that name (owner, 2026-11-23).

Take the working tree all the way to `main` in one go. Stop and report on any failure — never force past a failing hook, check, or merge.

## Options

- **`push`** (`/land push`): run this skill and then the `push` skill, in sequence, with no further question (owner, 2026-11-18). "Done" for the push is the end of this skill: the merge announced (step 7), or the step it stopped on. Send exactly one `PushNotification` as the `push` skill says, leading with the PR and its short description and the outcome (merged sha, or the failure and what the owner must do).

- **`end-to-end`** (`/land end-to-end`, or the owner says "end-to-end", "até o cluster", "entregar no cluster", "chegar no cluster"; owner, 2026-11-28): after step 7, run step 8, **Deliver**: the merge is done only when the change runs where the owner uses it. Plain `/land` stays as it is: the PRs merged, nothing deployed. The owner's word here is the go for the deploy, the kept cluster included (Nereus `docs/agent/rules.md`, "Production may break"), for this change only. It combines with `push`: the notification then waits for the delivery's outcome.

## Steps

1. **Commit** — follow the `commit` skill, with one exception: on a branch not yet merged, fold fixes to an existing commit into that commit (`git commit --amend` when it is `HEAD`, otherwise `git commit --fixup <sha>` + `GIT_SEQUENCE_EDITOR=: git rebase --interactive --autosquash main`). Where a commit-msg hook refuses a `fixup!` message (Nereus's Conventional Commits check), rebuild instead: `git reset --soft origin/main`, then recommit one commit per topic.

2. **Organize** — `git log --oneline main..HEAD` must show one Conventional Commit per topic. Squash or split until it does.

3. **Push** — `git push --force-with-lease --set-upstream origin <branch>`.

4. **PR** — detect the host via `git remote get-url origin`.
   - Write the description to `/tmp/<branch>-pr.txt` (markdown, repo-relative paths, `## Summary` + `## Test plan`; tick only the checks you actually ran).
   - Reuse an open PR for the branch if one exists (`gh pr list --head <branch>`); otherwise `gh pr create --base main --head <branch> --title "<conventional title>" --body-file /tmp/<branch>-pr.txt`.
   - Bitbucket, or `gh pr create` failed: show the compare/new-PR URL and stop — merge is manual there.

5. **Merge** — `gh pr merge <number> --rebase --delete-branch`. Never a merge commit.

6. **Sync** — `git checkout main && git pull --ff-only`.

7. **Announce** — `main` changed under every other session on this repository. List them (`ListAgents`; keep the ones whose working directory is this repository or one of its worktrees) and send each, with `SendMessage`, one `[release]`: the issue and PR with their short descriptions, the merged sha, the paths the merge changed (`git diff --stat <old-main>..origin/main`) and "rebase onto main". When the repository has its own protocol (Nereus: the `room` skill, `docs/agent/peers.md`), follow its format. No peer: send nothing.

8. **Deliver** (only with `end-to-end`) — take what merged to where it runs, then prove it there.
   - **Find the repository's own path**, never invent one: its agent docs first (Nereus: `docs/agent/publish.md` for `make release`, `docs/guides/operate/kept-cluster-update.md`, `scripts/deploy/live --help`; the kept cluster is `k3d-nereus`), then its `Makefile` and `scripts/`. Pick the smallest path that moves what changed: the CLI on the `PATH` (`make cli`), one image, or a release and the deploy (Nereus: `make release`, then `scripts/deploy/live --context k3d-nereus --allow-kept-cluster --chart-version <released>`). No path found: stop and report what is missing, never deploy by hand-built commands.
   - **Run the long commands in a new tmux window** of this session's tmux session (`tmux new-window -d -n deliver-<slug> -c <main clone>`, then `tmux send-keys`), each writing to a log named after the agent (`/tmp/<agent>-deliver.log`, `tee`), and show its `tail -f` line at once so the owner can follow from the phone. Commands that need the owner (an interactive login, a credential prompt) are handed over as `! <command>`, never typed for them.
   - **Credentials come from the existing logins** the docs name (Nereus: `GHCR_TOKEN="$(gh auth token)"` when it holds `write:packages`); never print them, never ask for a token in the chat.
   - **When the merge touched the repository's own CLI** (Nereus: any path under `cli/**`), update the CLI on the owner's `PATH` from the main clone after pulling it (Nereus: `make cli` in the main clone), then prove the `PATH` runs the new code with an output only the new version gives (`nereus --version` printing the released version, or an import check of the changed function), because on 2026-11-28 the `nereus` on the `PATH` was a fixed uv-tool copy of the previous release, so the delivered fix never ran on the owner's machine.
   - **Prove it live** with an output only the new change produces (the verification rule): the new version or commit the platform reports, the new field or text the change added, read from the running system (an API call, the page, `kubectl --context <ctx>` read-only). A smoke test that passed before the change too proves nothing alone.
   - **On failure, stop the line:** a broken deploy stops every other step until it is back (Nereus "Production may break"); report what broke, the log lines and the fix proposed, and never force past it (no `FORCE=1`, no `--reset-values`, no delete) without the owner's word.

## Report

- PR number with its title, and the merged commits (`<sha> <subject>`)
- Absolute path of `/tmp/<branch>-pr.txt`
- What was verified and what was not (e.g. syntax check only, service not enabled)
- The peers told (or none)
- With `end-to-end`: what was built and deployed (versions, digests or the release), the log path, the live proof (the command and the line it printed), or the step it stopped on
