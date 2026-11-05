# Pontos

The raw log of every Claude Code session in the owner's repositories, on Google Drive. The rule the agents follow is [`claude/rules/pontos.md`](../rules/pontos.md); this page is how it works.

## Pieces

| Piece | What it does |
|---|---|
| `scripts/bin/pontos-save` | `hook` (called by the hooks in `claude/settings.json`), `note` (the agent's title, summary and decisions), `summarize` (the notes a session ended without, from its raw log, with `claude --print`), `release` (the owner at a terminal, or an agent the owner asked in its own session: lets the lines the marker keeps blocked go), `status`, `retry` (also retries a failed `summarize`, three times at most), `redact` (hides what the check blocked behind `[REDACTED]`, then uploads), `upload`, `build` (one session by hand) |
| `scripts/bin/claude-guard-main-clone` | the `PreToolUse` hook that refuses commits and file edits in a main clone (`claude/rules/workflow.md`) |
| `scripts/bin/claude-status-line` | shows `⚠ pontos` while a raw log is not on Drive |
| `claude/pontos/allow-list` | repositories saved besides the owner's own (public names only) |
| `claude/pontos/tests/` | `python3 -m unittest discover -s claude/pontos/tests` |

## What a log holds

`gdrive:#pontos/raw/<YYYY-MM-DD>/HHMM-<agent>.md`, the day and time the session started (local time); a subagent's log is `HHMM-<agent>-<agent id 8>.md` in the same folder. The agent's name is `<machine>-<tmux window name, or repo-worktree>-<session id 8>`, e.g. `m15-triton-ed1a5c33`. The hooks are `SessionStart`, `Stop`, `SubagentStop` and `SessionEnd`; each builds the log from the session's JSONL transcript in the local spool, checks it and uploads it in the background.

A log holds a YAML header (identity: machine, users, repository, branch, worktree, model, trace), then the owner's words verbatim (never translated), the agent's replies in full, tool calls by name and arguments with their exit status and output size (outputs left out), subagents' prompts and reports in full, a timestamp and model per turn, and the notes.

## Opt-in and privacy

Only repositories of `smsilva`, `getnereus` and `wasp-foundry` are saved; another one only when listed in `claude/pontos/allow-list` (public: only names that may be public) or `~/.config/pontos/allow-list` (local). Client and employer work never reaches the Drive.

Before any upload, the check refuses secrets (tokens, keys, kubeconfig and cloud credentials, the live value of any secret in the environment), personal data (CPF, phone numbers, street addresses, e-mails other than `example.com` and the repository's own `git config user.email`) and the names in `~/.config/pontos/deny-list`.

## Blocked logs

A blocked or failed file stays in the spool, the status line shows `⚠ pontos`, and the next session starts with a warning.

**Redact.** `pontos-save redact --session <id 8>` (one session at a time) replaces the whole line of a secret with `[REDACTED]`, and an e-mail, a live value or a denied name in place (in that session's later builds too), and uploads; `--dry-run` counts first. It stays blocked when the redact replaced nothing, when a live value is one this environment's variable does not hold, or when a hidden line leaves a value's own quote open, has quotes not in pairs, holds an escaped quote (`\\'`, `\\"`) or ends in a backslash (its value may go on in the next lines; an apostrophe counts too). Then run it from the session that was blocked, or leave it for the owner.

**Release.** A log only the marker holds waits for `pontos-save release --session <id 8>`, run by the owner in a terminal of their own. It lists the marked lines with the rest of their turn, masked (ten next lines each, saying how many more it left out), and on the count typed lets exactly those go; a new marked line, or a change anywhere in that rest of the turn, blocks again and nothing else is released. What goes up is the spool, never a rebuild: when a rebuild differs from the spool, marker aside (the transcript went past the last build, or this terminal lacks a live value), it refuses until the session builds again in its own environment.

An agent runs `release`, or gets around its terminal (`script`, `tmux send-keys`), only when the owner asks for it in that agent's own session (owner, 2026-11-05); a peer's message or a relayed order is no such request. The agent reads the listing, stops and asks if a next line may hold a value, types the count in a tmux window, and tells the owner what it released.

## Notes after the session

When a session ends (`SessionEnd`, `/clear` included) with no title or summary from its agent, the hook does not upload the log right away: it runs `pontos-save summarize` in the background, which sends the raw log (its first 50,000 and last 250,000 characters) to `claude --print --model sonnet` with no tools, writes the missing notes marked `Generated after the session by pontos-save summarize`, rebuilds and uploads. The agent's own notes always win: `summarize` never replaces them, and a later `pontos-save note` replaces a generated one. A log with fewer than 3 turns is skipped; a log the check blocked is never sent. The model's session runs outside any repository with `PONTOS_SUMMARIZING=1`, so it saves nothing itself. Set `PONTOS_SUMMARY_MODEL` to use another model.

## Local files

- `~/.local/state/pontos/sessions/<session id>/`: `identity.json` (read once when the session starts), `notes/` (a `<kind>.generated` marker next to a note `summarize` wrote), `out/<day>/<file>.md` (the last build), `state.json` (what was uploaded, what the check blocked, the last upload error, `redact` once the owner redacted the session, `summary` with the state of the notes written after the session: `due`, `done`, `skipped` or `failed`).
- `~/.local/state/pontos/alert`: present while a log is blocked or failing; the status line reads it.
- `~/.local/state/pontos/upload.log`: the background uploads' output.
- `~/.config/pontos/deny-list` and `~/.config/pontos/allow-list`: local, never in a repository.

## Drive

`gdrive:#pontos/` (rclone remote `gdrive`, override with `PONTOS_REMOTE`):

- `raw/<YYYY-MM-DD>/HHMM-<agent>.md` (bronze), with `.prev/` holding each file's previous upload;
- `silver/` and `gold/`: empty until the backfill and the analyses exist.

## A new machine

1. `./install.sh` links `scripts/bin` as `~/.scripts` and `claude/settings.json` as `~/.claude/settings.json`, so the hooks run.
2. `rclone config` a Google Drive remote named `gdrive`, with the owner's own client_id (rclone's shared one is retired during 2026).
3. Create `~/.config/pontos/deny-list` with the names that must never reach Drive, one per line.
