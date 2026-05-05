---
name: note
description: Appends a note directly to the project CLAUDE.md file
---

The user invoked `/note` with some text as `<command-args>`. Append that text to the project's `CLAUDE.md` file.

Steps:
1. Read the current `CLAUDE.md` in the working directory
2. Append the note under a `## Notes` section at the end of the file — create the section if it doesn't exist
3. Each note should be a bullet (`- `) followed by the text verbatim
4. Write the updated file
5. Confirm with one short sentence what was added
