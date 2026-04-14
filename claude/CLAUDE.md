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

## Documentation

- Use `docs/` for markdown documentation files. Name them descriptively (e.g. `setup.md`, `networking.md`).
- Save technical decisions notes in `technical-decisions.md`.
- Use `next-steps.md` for actionable follow-up items discovered during sessions.
- When we have more than one document about the same topic, create a subfolder (e.g. `networking/`, `security/`) and place related docs inside it.
- When we have enough documentation, suggest the use of mkdocs to create a navigable site.
- When use mkdocs:
  - Ensure that all documentation files are linked in the `mkdocs.yml` navigation section, and that the site is generated without errors.
  - If the code is in github, suggest create a github actions to generate mkdocs site on push to main branch, and host it via github pages.
- `lessons-learned.md` for retrospective notes on what worked well and what could be improved during lab sessions and after.
- Não precisa mostrar o output de alteracoes de arquivos. Mostre apenas o resumo do que foi feito como Added 4 lines, removed 4 lines, modified 2 lines, etc.

## Code creation

- When creating code, ensure it is well-structured, modular, and follows best practices for the language and framework being used.
- Prioritize:
    - Python for microservices
    - Bash for scripts and automation
    - Terraform for infrastructure as code
    - Go for CLI tools and performance-critical components
    - Crossplane for multi-cloud infrastructure management
    - Helm Charts for Kubernetes application deployment

## Git

- No need to show the output of git commands, but show the command used
- Show the commit message when committing changes.

## Outputs

- IMPORTANT: Do not show long outputs. Use tail or head to show only the most relevant lines (5 at maximum).
- Saving local commands outputs to a file and sharing the file path instead. Eg: /tmp/sessions/2024-06-20-session1-command.txt
