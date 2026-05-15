---
name: dir-document
description: Use when asked to analyze, document, or create a CLAUDE.md for a specific directory or module — including "document this module", "analyze this directory", or before major changes to a subsystem. Accepts an optional output file argument; defaults to CLAUDE.md in the target directory.
---

# dir-document

Analyze a directory's architecture and produce a documentation file that gives future Claude sessions accurate, actionable context.

**Arguments:** `<dir>` (required) · `[output-file]` (optional — path for the output file; defaults to `<dir>/CLAUDE.md`)

## Workflow

### 1. Explore the directory

```bash
find <dir> -type f | sort
```

Read these files in priority order:
1. Entry points and public interfaces
2. Central abstractions or base classes
3. Configuration files
4. The largest or most-referenced source files

Skip generated files, build artifacts, and vendored code.

### 2. Analyze — answer these questions to drive Step 3

- **Purpose:** What problem does this module solve? Who calls it?
- **Architecture:** How is it structured? What are the layers or phases?
- **Key files:** Which files are entry points or central abstractions?
- **Patterns:** What conventions or idioms repeat throughout the code?
- **Dependencies:** What does this depend on externally? What depends on it internally?
- **Gotchas:** Non-obvious behaviors, edge cases, or landmines a reader would miss

### 3. Write `[output-file]` (default: `<dir>/CLAUDE.md`)

Target: under 50 lines. Include only what isn't obvious from reading the code.

```markdown
# <Module Name>

## Purpose
One sentence: what this module does and who uses it.

## Architecture
How it's structured — layers, phases, key abstractions.

## Key Files
- `filename` — role or responsibility
- `filename` — role or responsibility

## Patterns
- Recurring idiom or convention
- Another pattern

## Gotchas
- Non-obvious behavior or constraint
- Known landmine or edge case
```

Omit sections that have nothing non-obvious to say.

### 4. Report

After writing, output:
- What was documented and in which file
- Any ambiguities left unresolved (and why)
- Subdirectories that might benefit from their own CLAUDE.md
- If `[output-file]` was specified, add `@<output-file>` to the root CLAUDE.md under a
  relevant heading — a custom output path implies intent to `@`-import it. If using the
  default `<dir>/CLAUDE.md`, add `@<dir>/CLAUDE.md` to root only for core subsystems;
  otherwise it loads automatically whenever Claude accesses files in that directory.
