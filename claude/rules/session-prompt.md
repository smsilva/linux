# Session prompt

Each agent keeps the instructions for its next session, after `/clear`, in its own file (`<git common dir>/session-prompts/<agent name>.md`, outside the working tree), never in a shared `HANDOFF.local.md`; details in [`claude/session-prompt/README.md`](../session-prompt/README.md).

- **Before `/clear`** (and when the owner asks for "um prompt para depois do clear"): draft the prompt in the scratchpad and run `session-prompt save --file <draft>` without asking; show what was saved, then say the session can be cleared.
- **After `/clear`,** the hook puts the prompt in the session's context: follow it; when it says **STALE**, tell the owner first.
