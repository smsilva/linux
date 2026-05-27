# CLAUDE.md

## Overview

Personal Linux (Ubuntu 24.04) configuration and automation toolkit — bash configuration, 150+ utility scripts for Azure/AWS/Kubernetes/Docker/Terraform/Git, and installation scripts for development tools.

## Installation

```bash
./install.sh
```

Creates symlinks from `~/.scripts/` → `scripts/bin/`, links bash config files to home, sets up git templates, and runs tool-specific installers under `scripts/utilities/`.

## Key directories

- `scripts/bin/` — executable utility scripts (no `.sh` extension)
- `scripts/utilities/` — per-tool installation scripts (azure-cli, docker, kubectl, terraform, etc.)
- `scripts/git/hooks/` — git hooks; `commit-msg` enforces Conventional Commits format
- `claude/` — Claude Code config (symlinked to `~/.claude/`):
  - `skills/` — Claude Code skills; third-party skills are symlinks → `~/.git/{owner}/{repo}/`; registry at `claude/skills/third-party.md`
  - to reinstall third-party skills on a new machine: `/skill-from-github-repository-update bootstrap`
  - `agents/` — Claude Code custom agents
  - `CLAUDE.md` — global user instructions (symlinked to `~/.claude/CLAUDE.md`)
  - `settings.json` — global Claude settings
- `plugins/linux-tools/` — Claude Code plugin that publishes the `bash-scripts` and `conventional-commits` skills

## Conventions

- Bash scripts: use the `/bash-scripts` skill
- Commit messages: use the `conventional-commits` skill; format is enforced by the git `commit-msg` hook

## Bash configuration chain

On shell start: `.bashrc` → `scripts/bash_config` → `scripts/bash_functions` → `scripts/bash_aliases`

## settings.local.json only (not committed)

- enableAllProjectMcpServers
- enabledMcpjsonServers
- enabledPlugins
