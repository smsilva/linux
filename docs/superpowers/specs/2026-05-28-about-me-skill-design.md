# Skill `about-me` — Design

**Date**: 2026-05-28
**Status**: Approved for implementation
**Owner**: Silvio Silva

## Purpose

Give Claude Code on-demand access to Silvio's professional context so it can:

1. Write CVs, bios, LinkedIn posts, and talk abstracts in his voice.
2. Calibrate technical recommendations to his actual experience (e.g., "you've already used Crossplane in production — here's the next step").
3. Generate "about the speaker" sections for presentations and public materials.

## Non-goals

- Not a generic personal note system (use `note`/`note-user`).
- Not a CRM or contact book.
- No private/sensitive data in this iteration (no contacts, no salary, no addresses).

## Source data

- `~/Downloads/silvio-silva-linkedin.md` — extracted LinkedIn profile (canonical source for roles, dates, certifications, education).
- `~/Downloads/personal-work-journey-timeline.pdf` — visual timeline 1997–2026.
- `claude/CLAUDE.md` — working preferences (canonical source for tone/methods).

## File layout

```
claude/skills/about-me/
├── SKILL.md          # short entry point, pointer table to refs
├── timeline.md       # career 1997-present
├── stack.md          # current stack + levels + categories
├── credentials.md    # education + certifications
└── preferences.md    # tone, language, methods (mirrors CLAUDE.md)
```

All files in English (per `CLAUDE.md`: "Write Agent Skills in English"). Conversation with the user remains pt-BR; the skill content does not.

The skill lives under `claude/skills/about-me/` and is symlinked to `~/.claude/skills/about-me/` by the project's existing install flow.

## SKILL.md

Frontmatter:

```yaml
---
name: about-me
description: Use when writing a CV, bio, LinkedIn post, or talk abstract for Silvio; when calibrating technical recommendations to Silvio's experience ("do I have experience with X?"); or when an introduction or speaker section is needed. Loads timeline, stack, credentials, and preferences on demand via the pointer table.
---
```

Body (~25 lines):

- One-paragraph "Who" block: name, current role + company + start date, location, languages.
- Three-line "Current focus (2025-2026)" block.
- Three-line "Long-running domains" block.
- Pointer table mapping task → reference file.
- Instruction: "Read SKILL.md first. Then read ONLY the reference file(s) listed in the pointer table for the current task. Do not load all references unless the task spans multiple dimensions."

Pointer table:

| Task | File |
|---|---|
| CV, chronological bio, career journey, "I worked at X" | `timeline.md` |
| Calibrate technical recommendation, "do I know X?", current stack | `stack.md` |
| Certifications, education, "am I certified in X?" | `credentials.md` |
| Tone, language, working style, methods | `preferences.md` |

## timeline.md

One section per role, newest first. Each section has:

- Heading: `## Company — Role (MM/YYYY – MM/YYYY, Location, Modality)`.
- English summary bullets (canonical; Claude uses these by default).
- Optional collapsible appendix `<details><summary>Original (pt-BR)</summary>…</details>` preserving LinkedIn bullets verbatim for direct quoting.

Roles to include (from LinkedIn, deduplicated against PDF):

1. CI&T — Developer Master (09/2022 – Present, Belo Horizonte/MG, Hybrid)
2. CI&T — Systems Architect (04/2021 – 09/2022, Belo Horizonte/MG)
3. CI&T — Software Engineer (11/2019 – 04/2021, Belo Horizonte)
4. Optum — Senior Software Developer / Tech Lead (05/2016 – 11/2019, Belo Horizonte/MG)
5. MedAlliance Net — Senior Systems Analyst (02/2009 – 04/2016, Recife)
6. CSI — Comércio Soluções Inteligentes — Technical Lead (02/2008 – 01/2009, Recife)
7. OPS Planos de Saúde — Development Coordinator (01/2006 – 01/2008, Recife)
8. Inteligência Informática — Programmer (2003 – 2005, Recife)
9. Apply Solutions — Programmer (2002 – 2003, Recife)
10. Policlínica Santa Clara — Programmer (1999 – 2002, Recife)
11. Layout Informática — Instructor (06/1997 – 04/1999, Recife)

End of file: a one-line "Career arc" summary — "Recife (1997-2008) → Belo Horizonte (2009-present); healthcare domain throughout; pivoted to cloud engineering and AI tooling from 2019 onward."

## stack.md

Categorized, with confidence level (`expert` / `strong` / `familiar` / `learning`). Levels are inferred from years of evidence + recency in the LinkedIn bullets.

Categories:

- **Cloud**: Azure (expert), AWS (strong), OpenStack (familiar).
- **Kubernetes & Platform**: Kubernetes (expert), Crossplane + KCL (familiar), Backstage, GitHub Enterprise, Bitbucket.
- **IaC**: Terraform / Stacks (expert), Ansible (strong).
- **Languages**: Java/J2EE (expert, 15+ years), Bash (expert), Python (strong, growing focus), SQL/PL-SQL (strong), Delphi (legacy).
- **AI & Agents (2026 focus)**: Claude Code, MCP, agent skills, RAG, Agno, Pydantic, prompt engineering.
- **Messaging**: Apache Kafka + Spring Integration + KEDA, JMS/ActiveMQ.
- **Observability**: Prometheus, New Relic, Azure Monitor.
- **Domain expertise**: healthcare (15+ years — telemedicine, health insurance, telehealth, population risk), retail automation, multi-tenant B2B SaaS.

Each entry is a single line; rationale (where the experience comes from) lives in `timeline.md`, not here.

## credentials.md

Sections:

- **Education**: postgraduate (CESAR EDU 2011–2012), bachelor (Universidade Salgado de Oliveira 2002–2005).
- **Active certifications (2026)**: 5 entries (Claude 101, agent skills intro, MCP intro, Claude Code in Action, Desenvolvendo Agentes de IA / Visie).
- **Expired**: CKA (Linux Foundation 12/2020 → 12/2023).
- **Alura courses**: one-line aggregate ("34 courses, ~400h on Java/EJB/Maven/SOLID/Design Patterns/Java 8/Android — full list in LinkedIn"), no per-course detail to keep the file scannable.

## preferences.md

Mirrors the canonical preferences from `claude/CLAUDE.md`, condensed and reformatted for skill consumption:

- **Communication**: concise, actionable, no preamble, no hedging.
- **Languages**: conversation in pt-BR; written artifacts (skills, docs, code comments) in English; never translate technical terms.
- **Methods**: Walk Skeleton, TDD when applicable, Conventional Commits.
- **Tooling**: bash scripts under `~/git/linux/scripts/bin/`, Claude Code, Ubuntu 24.04.

Note at the top: "Canonical source is `claude/CLAUDE.md` — this is a summary scoped to introductions and recommendations. If they diverge, `CLAUDE.md` wins."

## Testing / acceptance

The skill is considered working when:

1. Asking Claude "what's my background with Crossplane?" triggers `about-me` → reads `stack.md` and `timeline.md` (CI&T Developer Master section) → answers with the Crossplane+KCL bullet from the CI&T role.
2. Asking "write me a 3-sentence bio for a TDC talk submission" reads `SKILL.md` only, produces a bio mentioning Developer Master at CI&T + cloud/AI focus + healthcare background.
3. Asking "do I have a CKA?" reads `credentials.md` and reports it as expired in 2023.
4. The skill does not auto-load when the conversation is unrelated (e.g., a bash script edit).

## Out of scope / future work

- Private contact data (separate `about-me-private` skill if needed).
- Auto-sync from LinkedIn (one-shot import for now; refresh manually).
- GitHub stats / talk recordings / publications (add to `stack.md` or a new `public-work.md` when needed).
