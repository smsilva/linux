---
name: save-session-learnings
description: Use when ending a session to persist project knowledge, user corrections, and inferred details from the conversation into the appropriate CLAUDE.md files.
---

## Workflow

### 1. Scan for lasting learnings

Look for:
- Facts about the project not derivable from the code alone
- Corrections the user made to generated code or explanations
- Implementation details that required inference or research
- Gotchas or non-obvious behaviors discovered
- Architectural or design decisions explained by the user
- Patterns or conventions that weren't obvious upfront

### 2. Filter — only what has lasting value

| Keep | Discard |
|------|---------|
| Project-specific patterns and constraints | One-off fixes unlikely to recur |
| Corrected misconceptions about the codebase | Anything obvious from reading the code |
| Non-obvious gotchas and landmines | Standard practices already documented elsewhere |
| Architectural decisions with context | Temporary state from this session |

### 3. Route to the right file

| Content type | File |
|---|---|
| Shared project knowledge (team-wide) | `CLAUDE.md` in the nearest relevant directory |
| Personal setup, local paths, dev preferences | `CLAUDE.local.md` in the project root |
| User-wide preferences across all projects | `~/.claude/CLAUDE.md` |

When in doubt, use the `CLAUDE.md` closest to the code the learning refers to. A learning about a specific subdirectory belongs in that subdirectory's `CLAUDE.md`, not the root.

### 4. Write concise entries

Each entry must be:
- One or two sentences max
- Actionable — tells Claude what to do or watch out for, not just what exists
- Placed in the most relevant existing section; create a new section only if none fits
- Written in imperative or declarative form ("Always use X", "Avoid Y", "The Z field is...")

Do not add boilerplate or verbose explanations. If a reader would understand it by reading the code, skip it.

### 5. Report

After updating, print:
```
Updated: <file> — <entry>
Updated: <file> — <entry>
Discarded: <topic> (<reason>)
```