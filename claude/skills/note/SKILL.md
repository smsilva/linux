---
name: note
description: Appends a note to a CLAUDE.md file. Defaults to the project CLAUDE.md; pass a file path as the first argument to override.
---

**Determining the target file:**
- If `<command-args>` starts with a file path (absolute or `~/`-prefixed), use it as target; treat the remainder as the note text.
- If a target was already used this session, reuse it without asking.
- Otherwise, default to `CLAUDE.md` in the current working directory.

Steps:
1. Determine the target file (see above).
2. Read the target file.
3. Find the most relevant section and insert the note there; if unrelated to any section, append at the end.
4. Write the updated file.
5. If the modified section is too big, create a file under docs/<topic-name>/section-topic-name.md, move the section there, and link to it from the main file.
6. Confirm with one short sentence what was added and to which file.
