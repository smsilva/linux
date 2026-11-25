# Session prompt

Each agent keeps the instructions for its next session in its own file (`session-prompt`, details in [`claude/session-prompt/README.md`](../session-prompt/README.md)); `next save` writes it before `/clear`. After `/clear`, the hook puts the prompt in the session's context: follow it; when it says **STALE**, tell the owner first.
