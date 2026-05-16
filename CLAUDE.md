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
- `claude/` — Claude Code config (symlinked to `~/.claude/` by `install.sh`):
  - `skills/` — Claude Code skills; skills de terceiros são symlinks → `~/.git/{owner}/{repo}/`; registry em `claude/skills/third-party.md`
  - para reinstalar skills de terceiros em máquina nova: `/skill-from-github-repository-update bootstrap`
  - `agents/` — Claude Code custom agents
  - `CLAUDE.md` — global user instructions (symlinked to `~/.claude/CLAUDE.md`)
  - `settings.json` — global Claude settings
- `plugins/linux-tools/` — Claude Code plugin that publishes the `bash-scripts` and `conventional-commits` skills

## Bash script conventions

Use `/bash-scripts` skill when creating new scripts.

## Commit message conventions

Use the `conventional-commits` skill. Format is enforced by the git `commit-msg` hook.

## Bash configuration chain

On shell start: `.bashrc` → `scripts/bash_config` → `scripts/bash_functions` → `scripts/bash_aliases`

## settings.local.json only (not committed)

- enableAllProjectMcpServers
- enabledMcpjsonServers
- enabledPlugins
