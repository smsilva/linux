---
board: none
repository: smsilva/linux
---
# Next

The queue of this repository is its open issues (no board). Read by the global `next` skill (`claude/skills/next/SKILL.md`).

A design here covers, per deliverable:

- **Script:** the command and its options as the owner types them, following the `bash-scripts` skill (no extension, long options, help text); new scripts go in `scripts/bin/`, per-app files in `apps/<app>/`.
- **Test:** its test in `scripts/tests/` (Python `unittest`), asserting on an output only the change produces; tests that render state run with an isolated `XDG_STATE_HOME` and `HOME`.
- **Doc:** the README, `SKILL.md` or rule it changes (`claude/rules/` for global instructions, one topic per file).
- **Try it live:** how the owner sees it working before the PR (a wrapper, a tmux pane, a Multipass VM for installers).
- **Machine effects:** what it writes outside the repository (`~/.claude/`, `~/.local/state/`, symlinks from `install.sh`) and how to undo it.
