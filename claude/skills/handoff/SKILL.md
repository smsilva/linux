---
name: handoff
description: Create or update a handoff document so the next agent with fresh context can continue the work
---

1. If `HANDOFF.md` exists, read it before proceeding.

2. Run `git log main..HEAD` to capture work since the last update.

3. Write `HANDOFF.md` in the project root with:
   - **Goal**: What we're trying to accomplish
   - **Current Progress**: What's been done so far
   - **What Worked**: Approaches that succeeded
   - **What Didn't Work**: Approaches that failed
   - **Next Steps**: Clear action items for continuing

4. Tell the user the file path.
