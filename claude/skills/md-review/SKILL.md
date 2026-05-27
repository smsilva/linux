---
name: md-review
description: Use when reviewing or tightening a Markdown file that will be read by an agent (SKILL.md, CLAUDE.md, custom agent prompts, slash-command instructions) to make it more discoverable, imperative, and token-efficient. Accepts a file path or a skill name (e.g. "handoff").
---

# md-review

## Scope

This skill reviews `.md` files **consumed by agents**, not human-facing docs (READMEs, blog posts, design docs).

Goal: make the file produce better agent behavior — discoverable, decidable, cheap in tokens.

## When NOT to use

- Human-facing docs (README, CHANGELOG, design docs) — different audience, different criteria.
- New SKILL.md from scratch — use `superpowers:writing-skills` (it covers authoring with TDD).

## Step 1 — Resolve the file

- Path ending in `.md` or containing `/`: use directly.
- Bare name (no `/`, no `.md`): treat as a skill name, resolve to `~/.claude/skills/{name}/SKILL.md`.

## Step 2 — Pick the right reviewer

```
Is the file a SKILL.md?
├── yes → delegate criteria to superpowers:writing-skills (CSO, frontmatter, token budget,
│         anti-patterns, rationalization tables). Apply the checklist in Step 3 on top.
└── no  → apply only the checklist in Step 3.
```

## Step 3 — Review checklist (agent-facing criteria)

Go through every item. Flag what fails.

**Discoverability**
- Does the description/title contain the keywords an agent would search for (errors, symptoms, tool names)?
- For SKILL.md: does the description start with "Use when…" and avoid summarizing the workflow? (See `superpowers:writing-skills` § CSO.)

**Imperative tone**
- Are instructions direct commands ("Run X", "Read Y") instead of prose ("You might want to consider…")?
- Is each step decidable without the agent having to infer intent?

**Token cost**
- Any sentence that could be deleted without losing a decision the agent needs to make? Delete it.
- Repeated content that could be a single cross-reference?
- Examples longer than the rule they illustrate?

**Cross-references**
- No `@path/to/file` syntax — it force-loads and burns context. Use plain skill names or relative paths.
- Reference other skills by name with an explicit marker: `**REQUIRED:** Use {skill-name}`.

**Loopholes (for rule-enforcing files)**
- Every rule has a counter-rationalization. Add a "Red flags" or rationalization table if missing.

**Language**
- Written in English. If pt-BR, flag for translation (per global rule "Write Agent Skills in English").
- Technical terms kept untranslated (API, endpoint, commit, parse, cache).

**Structure hygiene**
- Flowcharts only for non-obvious decisions, never for linear steps or reference data.
- One excellent example, not the same example in three languages.
- No narrative storytelling ("Last session we found…").

## Step 4 — Report and confirm

List findings as a table: `location | issue | proposed fix`. Ask before editing.

## Step 5 — Apply

Use Edit for each approved change. Do not rewrite the whole file in one Write call unless the user asks.