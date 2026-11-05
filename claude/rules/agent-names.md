# Agent names

The owner's rule for every repository (2026-10-31): **every agent session on this machine has a unique name**, given by the `SessionStart` hook (`agent-name hook`), which puts "Your name is <name>" in the session's context. The lists, the configuration, the rotation and the launcher: [`claude/agent-names/README.md`](../agent-names/README.md).

- **Know it and say it:** when the owner asks your name, answer with it. Sign cross-session messages, orders and replies with it when relevant. A subagent has no name of its own: it works under its session's.
- **Look it up:** `agent-name whoami --session-id <id>`; `agent-name list` shows every name in use.
- A repository's own naming rule for sessions (a tmux window name) gives way to this one.
