---
name: note
description: Appends a note to a CLAUDE.md file. Defaults to the project CLAUDE.md; pass a file path as the first argument to override.
---

The user invoked `/note` with `<command-args>`. Append the note text to a CLAUDE.md file.

**Determining the target file:**
- If `<command-args>` starts with a file path (absolute or `~/`-prefixed), use it as target; treat the remainder as the note text.
- If a target was already used this session, reuse it without asking.
- Otherwise, default to `CLAUDE.md` in the current working directory.

Steps:
1. Determine the target file (see above).
2. Read the target file (create if missing).
3. If target is `CLAUDE.local.md` and `.gitignore` does not contain it, offer to add it.
4. If the file has existing content, find the most relevant section and insert the note there. If the note is unrelated to any existing content, append it at the end with a minimal header for context.
5. Write the updated file.
6. Confirm with one short sentence what was added and to which file.