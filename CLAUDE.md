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

Use `/bash-scripts` skill when creating new scripts. Key rules:

- No file extension on executables
- 2-space indent; opening `do`/`then` on same line as `while`/`if`
- Lowercase local variables (`input_file`, `dry_run`); UPPERCASE env vars (`ARM_SUBSCRIPTION_ID`)
- Always quote variable expansions: `"${variable}"` not `$variable`
- Support stdin/file fallback: `input_file="${1:-/dev/stdin}"`
- Use `${var?}` for required argument validation (fails fast with clear error)
- Add script's own directory to `$PATH` to reference sibling scripts
- Show only a short prefix when printing secrets: `"${SECRET:0:3}"`
- Use `set -e` only for scripts with sequential steps that must all succeed
- Use long-form CLI options: `--yes` not `-y`, `--verbose` not `-v`, `--output` not `-o`

## Commit message conventions

Use `/conventional-commits` skill when writing commits. All commits must follow Conventional Commits:

```
<type>(<scope>): <description>
```

- Types: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `ci`, `perf`, `revert`
- Scope: most specific relevant path or identifier (`scripts/bin/arm`, `scripts/bash_config`)
- Description: imperative mood, lowercase, no period, under 72 chars total
- Breaking changes: append `!` — `feat(api)!: remove endpoint`

This is enforced by the git `commit-msg` hook.

## Bash configuration chain

On shell start: `.bashrc` → `scripts/bash_config` (PATH, env vars) → `scripts/bash_functions` (padding helpers) → `scripts/bash_aliases` (Git, Docker, K8s, Azure shortcuts)

### This file evolution

Update this file as needed to provide guidance to Claude when working with this codebase. It should serve as a living document to help maintain consistency and best practices across all contributions.
