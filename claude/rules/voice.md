# Voice

`speak "text"` reads text aloud in pt-BR with Piper (`scripts/bin/speak`).

- Default: never call `speak`
- Start speaking only after the owner asks for it in the current session, and only from the main session; stop when asked
- Subagents, background agents, and workflows never speak
- Exception: announce by voice that an agent finished only when the owner explicitly asks for it in that session
- When speaking, say one or two short sentences in pt-BR (the outcome), not the full reply
