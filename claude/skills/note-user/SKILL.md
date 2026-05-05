---
name: note-user
description: Appends a note directly to the user's global CLAUDE.md file (~/.claude/CLAUDE.md)
---

The user invoked `/note-user` with some text as `<command-args>`. Append that text to the user's global `~/.claude/CLAUDE.md` file.

Steps:
1. Read `~/.claude/CLAUDE.md`
2. Append the note under a `## Notes` section at the end of the file — create the section if it doesn't exist
3. Each note should be a bullet (`- `) followed by the text verbatim
4. Write the updated file
5. Confirm with one short sentence what was added
