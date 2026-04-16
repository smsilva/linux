# Claude Instructions

## General
- Concise responses, actionable
- No preamble ("Sure!", "Great question!") or closing summaries
- No narration before tool calls
- Don't restate the question
- One solution unless alternatives are requested
- Skip hedging phrases ("Note that...", "Keep in mind...")
- Explain only non-obvious logic

## Bash scripts
- No file extension on executables
- Long-form CLI options (`--yes`, not `-y`)
- 2-space indent; `do`/`then` on same line as `while`/`if`
- Lowercase locals; UPPERCASE env vars
- Always quote: `"${variable}"`
- stdin fallback: `input_file="${1:-/dev/stdin}"`
- Required args: `${var?}`

## Commits
Use `conventional-commits` skill.

## Documentation
- `docs/` for markdown; descriptive names (`setup.md`, `networking.md`)
- `technical-decisions.md` for ADRs; `next-steps.md` for follow-ups; `lessons-learned.md` for retros
- Related docs → subfolder (`networking/`, `security/`)
- mkdocs: link all docs in nav; add GH Actions for Pages if on GitHub
- File change output: summary only (e.g. "Added 4 lines, removed 2")

## Code — language priorities
- Python → microservices
- Bash → scripts/automation
- Terraform → IaC
- Go → CLI/performance
- Crossplane → multi-cloud infra
- Helm → Kubernetes deployments

## Git & outputs
- Git: show command and commit message; omit command output
- Outputs: max 5 lines; save long output to `/tmp/<topic>/YYYY-MM-DD_HHMMSS-<name>.txt`; share path

## Tests
- Track runs in `.tests.md` (timestamp + commit hash); add to `.gitignore`
- Before a new commit, check for changes since last run
- Never commit if tests were failing, unless explicitly instructed
