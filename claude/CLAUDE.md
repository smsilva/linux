# Global Claude Instructions

## General preferences

- Concise responses, but with enough detail to be actionable

## Bash scripts

Conventions:

- No file extension on executables (e.g. `deploy`, not `deploy.sh`)
- Use long-form CLI options: `--yes` not `-y`, `--verbose` not `-v`, `--output` not `-o`
- 2-space indent; opening `do`/`then` on same line as `while`/`if`
- Lowercase local variables (`input_file`, `dry_run`); UPPERCASE env vars
- Always quote variable expansions: `"${variable}"` not `$variable`
- Support stdin/file fallback: `input_file="${1:-/dev/stdin}"` or `input=$(cat)`
- Use `${var?}` for required argument validation

## Commit messages

Follow Conventional Commits: `<type>(<scope>): <description>`

Types: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `ci`, `perf`, `revert`
