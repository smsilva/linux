# CLAUDE.md

## Overview

Personal Linux (Ubuntu 24.04) configuration and automation toolkit: bash configuration, utility scripts and tool installers. Install with `./install.sh`.

## Non-obvious layout

- `claude/` is symlinked to `~/.claude/` (skills, rules, agents, `settings.json`, `CLAUDE.md`)
- Third-party skills in `claude/skills/` are symlinks → `~/.git/{owner}/{repo}/`; registry at `claude/skills/third-party.md`; reinstall them on a new machine with `/skill-from-github-repository-update bootstrap`
- `claude/archived/skills/` holds skills out of use, outside what Claude Code scans; how to bring one back in its `README.md`
- `apps/<app>/config/` holds a sanitized snapshot of the app's config: no passwords, keys or install IDs, since the repo is public (`apps/README.md`)

## Conventions

- Bash scripts: use the `/bash-scripts` skill
- Commit messages: use the `conventional-commits` skill; format is enforced by the git `commit-msg` hook

## Bash configuration chain

On shell start: `.bashrc` → `scripts/bash_config` → `scripts/bash_functions` → `scripts/bash_aliases`

## settings.local.json only (not committed)

- enableAllProjectMcpServers
- enabledMcpjsonServers
- enabledPlugins

## Next work

Move the per-tool installers from `scripts/utilities/` into `apps/<app>/` (`apps/<app>/install` is a symlink to the old installer until then): plan and order in #34.
