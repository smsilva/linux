# Agent names

Every agent session on this machine gets a unique name from the `SessionStart` hook (`agent-name hook`); it wins over a repository's own session-naming rule, and a subagent works under its session's name. `agent-name whoami --session-id <id>` and `agent-name list` look names up; details in [`claude/agent-names/README.md`](../agent-names/README.md).
