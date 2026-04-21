---
name: handoff
description: Create or update a handoff document so the next agent with fresh context can continue this work.
---

Steps:

1. Check if HANDOFF.md already exists in the project

2. If it exists, read it first to understand prior context before updating

3. Read the latest commits until main branch to gather any new information or progress that has been made since the last handoff document was created or updated.

4. Create or update the document with all information below based on the current:
   - **Goal**: What we're trying to accomplish
   - **Current Progress**: What's been done so far
   - **What Worked**: Approaches that succeeded
   - **What Didn't Work**: Approaches that failed (so they're not repeated)
   - **Next Steps**: Clear action items for continuing

Save as HANDOFF.md in the project root and tell the user the file path so they can start a fresh conversation with just that path.
