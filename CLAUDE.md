# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

Personal Linux (Ubuntu 24.04) configuration and automation toolkit — bash configuration, ~140 utility scripts for Azure/AWS/Kubernetes/Docker/Terraform/Git, and installation scripts for development tools.

## Installation

```bash
./install.sh
```

Creates symlinks from `~/.scripts/` → `scripts/bin/`, links bash config files to home, sets up git templates, and runs tool-specific installers under `scripts/utilities/`.

## Key directories

- `scripts/bin/` — ~140 executable utility scripts (no `.sh` extension)
- `scripts/utilities/` — per-tool installation scripts (azure-cli, docker, kubectl, terraform, etc.)
- `scripts/git/hooks/` — git hooks; `commit-msg` enforces Conventional Commits format
- `claude/skills/` — Claude Code skills: `bash-scripts` and `conventional-commits`

## Bash script conventions

Use `/bash-scripts` skill when creating new scripts.

## Commit message conventions

Use the `conventional-commits` skill. Format is enforced by the git `commit-msg` hook.

## Bash configuration chain

On shell start: `.bashrc` → `scripts/bash_config` (PATH, env vars) → `scripts/bash_functions` (padding helpers) → `scripts/bash_aliases` (Git, Docker, K8s, Azure shortcuts)

### This file evolution

Update this file as needed to provide guidance to Claude when working with this codebase. It should serve as a living document to help maintain consistency and best practices across all contributions.

## Changes only on settings.local.json

- enableAllProjectMcpServers
- enabledMcpjsonServers
- enabledPlugins
