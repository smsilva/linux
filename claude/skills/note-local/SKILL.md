---
name: note-local
description: Appends a note directly to the project's local CLAUDE.local.md file (not committed to git)
---

The user invoked `/note-local` with some text as `<command-args>`. Append that text to `CLAUDE.local.md` in the current working directory.

Steps:
1. Read `CLAUDE.local.md` if it exists; otherwise start with an empty file
2. Append the note under a `## Notes` section at the end of the file — create the section if it doesn't exist
3. Each note should be a bullet (`- `) followed by the text verbatim
4. Write the updated file
5. Confirm with one short sentence what was added
