# Working preferences

> Canonical source: `~/.claude/CLAUDE.md`. This is a summary scoped to introductions and recommendations. If they diverge, `CLAUDE.md` wins.

## Communication

- Concise, actionable; no preamble ("Sure!", "Great question!"); no hedging ("Note that…", "Keep in mind…").
- Don't restate the question. Explain only non-obvious logic.

## Languages

- **Conversation:** pt-BR.
- **Written artifacts** (skills, docs, code comments): English.
- Never translate technical terms (API, endpoint, commit, push, pull request, cache, parse, GitOps).

## Methods

- **Walk Skeleton** — ship a thin end-to-end slice early for feedback.
- **TDD** when applicable.
- **Conventional Commits** — enforced by the git `commit-msg` hook.

## Tooling

- Bash scripts under `~/git/linux/scripts/bin/` (conventions in the `bash-scripts` skill).
- Claude Code as primary AI dev tool.
- Ubuntu 24.04.
