# Pontos

Pontos is the raw data layer: every Claude Code session in one of the owner's repositories leaves its raw log on Google Drive, for data analysis later (in Hesiod's *Theogony*, Pontos is the primordial sea, father of Nereus).

- **The hooks write it, not the agent:** `SessionStart`, `Stop`, `SubagentStop` and `SessionEnd` in `settings.json` run `pontos-save hook`, which builds the log from the session's JSONL transcript in a local spool (`~/.local/state/pontos/`), checks it, and uploads it in the background. Nothing to do per turn.
- **Where:** `gdrive:#pontos/raw/<YYYY-MM-DD>/HHMM-<agent>.md`, the day and time the session started (local time); a subagent's log is `HHMM-<agent>-<agent id 8>.md` in the same folder. `#pontos/silver` and `#pontos/gold` come later (medallion architecture). The previous upload of a file is kept in `.prev/`.
- **The agent's name:** `<machine>-<tmux window name, or repo-worktree>-<session id 8>`, e.g. `m15-triton-ed1a5c33`.
- **What it holds:** a YAML header (identity: machine, users, repository, branch, worktree, model, trace), then the owner's words verbatim (never translated), the agent's replies in full, tool calls by name and arguments with their exit status and output size (outputs left out), subagents' prompts and reports in full, a timestamp and model per turn.
- **The agent's part, only what needs judgement:** at a milestone and before the session ends (a session that ends without them gets notes from `pontos-save summarize`, a model reading the raw log, marked as generated; the agent's own are better and always win), write a title, a summary (with a `Radar: <ring> · <idea>` line per idea created or moved) and the decisions taken, each from a file or stdin:

```bash
pontos-save note title --file /tmp/title.md
pontos-save note summary --file /tmp/summary.md
pontos-save note decisions --file /tmp/decisions.md
```

- **Opt-in:** only repositories of `smsilva`, `getnereus` and `wasp-foundry` are saved; another one only when listed in `claude/pontos/allow-list` (public: only names that may be public) or `~/.config/pontos/allow-list` (local). Client and employer work never reaches the Drive.
- **Privacy:** before any upload, the check refuses secrets (tokens, keys, kubeconfig and cloud credentials, the live value of any secret in the environment), personal data (CPF, phone numbers, street addresses, e-mails other than `example.com` and the repository's own `git config user.email`) and the names in `~/.config/pontos/deny-list` (local, never in a repository: the employer's and clients' names). Never print the environment into a session.
- **When it fails:** a blocked or failed file stays in the spool, the status line shows `⚠ pontos`, and the next session starts with a warning: tell the owner, then run `pontos-save status`. `pontos-save retry` uploads what was left. When the owner says what was flagged may go with its value hidden, `pontos-save redact --session <id 8>` (one session, only on the owner's word) replaces it with `[REDACTED]` (in that session's later builds too) and uploads; `--dry-run` counts first.
