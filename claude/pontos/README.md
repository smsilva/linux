# Pontos

The raw log of every Claude Code session in the owner's repositories, on Google Drive. The rule the agents follow is [`claude/rules/pontos.md`](../rules/pontos.md); this page is how it works.

## Pieces

| Piece | What it does |
|---|---|
| `scripts/bin/pontos-save` | `hook` (called by the hooks in `claude/settings.json`), `note` (the agent's title, summary and decisions), `status`, `retry`, `upload`, `build` (one session by hand) |
| `scripts/bin/claude-guard-main-clone` | the `PreToolUse` hook that refuses commits and file edits in a main clone (`claude/rules/workflow.md`) |
| `scripts/bin/claude-status-line` | shows `⚠ pontos` while a raw log is not on Drive |
| `claude/pontos/allow-list` | repositories saved besides the owner's own (public names only) |
| `claude/pontos/tests/` | `python3 -m unittest discover -s claude/pontos/tests` |

## Local files

- `~/.local/state/pontos/sessions/<session id>/`: `identity.json` (read once when the session starts), `notes/`, `out/<day>/<file>.md` (the last build), `state.json` (what was uploaded, what the check blocked, the last upload error).
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
