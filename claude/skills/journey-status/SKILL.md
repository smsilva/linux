---
name: journey-status
description: Use when the owner asks which journeys are open and how far each one is ("quais são as jornadas abertas", "status das jornadas", "progresso das jornadas", "como estão as jornadas", "/journey-status", "journey status"). Lists the repository's open issues labelled `journey` with the progress `journey-status` computes from GitHub's sub-issue counts, and adds one short pt-BR description per journey. Read-only on GitHub.
---

# Journey status

A journey is an open issue labelled `journey` whose sub-issues are its steps (getnereus/nereus `docs/agent/journeys.md`). Its progress is the closed sub-issues over all of them, which `journey-status` reads from the summary GitHub keeps on the parent issue: the agent never counts on its own, it only writes the description.

## Steps

1. From the repository, run `journey-status --json` (add `--repo <owner/name>` when the session is elsewhere). A failing `gh` is reported as is; nothing is guessed.
2. Write one short pt-BR description per journey from its title (a few words of the goal, never the whole title); read the issue body only when the title is not enough.
3. Answer with one block per journey, most advanced first, laid out for a phone (owner, 2026-11-24: a code block wraps mid-line there, and bold lines with blank paragraphs run together): an H3 heading with the number, a ten-cell bar (`▰` per tenth done, rounded, `▱` for the rest) and the whole percentage; under it, the description with the count in parentheses. No code block.

   ```markdown
   ### #1725 ▰▰▰▰▰▰▱▱▱▱ 60%
   Apresentações: papéis e direitos, depois o perfil de palestras (3/5)
   ```

   A journey with no sub-issues says `sem passos` instead of the bar and the count. Close, after a `---` rule, with one line: how many are open against the soft limit of about three active journeys, and which journey is a step of another.

## Rules

- Read-only: never claim, comment, label or change the board here.
- The detail per step (which sub-issue is open, who owns it) only when the owner asks for it: `gh issue view <n>` and the parent's sub-issues.
