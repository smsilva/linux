# Pontos

The raw log of every Claude Code session in the owner's repositories, on Google Drive. The rule the agents follow is [`claude/rules/pontos.md`](../rules/pontos.md); this page is how it works.

## Pieces

| Piece | What it does |
|---|---|
| `scripts/bin/pontos-save` | `hook` (called by the hooks in `claude/settings.json`), `note` (the agent's title, summary and decisions), `summarize` (the notes a session ended without, from its raw log, with `claude --print`), `release` (the owner at a terminal, or an agent the owner asked in its own session: lets the lines the marker keeps blocked go), `status`, `retry` (also retries a failed `summarize`, three times at most), `redact` (hides what the check blocked behind `[REDACTED]`, then uploads), `upload`, `build` (one session by hand) |
| `scripts/bin/claude-guard-main-clone` | the `PreToolUse` hook that refuses commits and file edits in a main clone (`claude/rules/workflow.md`) |
| `scripts/bin/claude-status-line` | shows `⚠ pontos` while a raw log is not on Drive |
| `scripts/bin/pontos-classification-check` | the daily deterministic check of the voice notes' classification, with a report in silver (see below) |
| `scripts/bin/pontos-extract-refs` | the fixed extraction of a note's `to_refs`, `issue_refs` and `source_urls`, for the classification routine (see below) |
| `scripts/utilities/pontos/` | the systemd user timer of the check, daily at 05:30 (`install.sh`) |
| `claude/pontos/allow-list` | repositories saved besides the owner's own (public names only) |
| `claude/pontos/tests/` | `python3 -m unittest discover -s claude/pontos/tests` |

## What a log holds

`gdrive:#pontos/raw/<YYYY-MM-DD>/HHMM-<agent>.md`, the day and time the session started (local time); a subagent's log is `HHMM-<agent>-<agent id 8>.md` in the same folder. The agent's name is `<machine>-<tmux window name, or repo-worktree>-<session id 8>`, e.g. `m15-triton-ed1a5c33`. The hooks are `SessionStart`, `Stop`, `SubagentStop` and `SessionEnd`; each builds the log from the session's JSONL transcript in the local spool, checks it and uploads it in the background.

A log holds a YAML header (identity: machine, users, repository, branch, worktree, model, trace), then the owner's words verbatim (never translated), the agent's replies in full, tool calls by name and arguments with their exit status and output size (outputs left out), subagents' prompts and reports in full, a timestamp and model per turn, and the notes.

## What else lives in `#pontos`

- `#pontos/raw/<YYYY-MM-DD>/` also holds the owner's voice notes, `HHMM-voice-<slug>`, next to the Claude Code logs; the classification of a note is its sibling `HHMM-voice-<slug>-classification.md`.
- `#pontos/silver/classification/` holds the daily classification run (rules, state and reports).
- `#pontos/beach/` holds the work orders and the material shared with the voice session (`replies/`, `opinions/`, `proposals/`, `references/`, `bridge/`); it replaces the Drive folder `dump-mental-prompts`, removed on 2026-11-08.

## Classification check

`pontos-classification-check` checks the classification of the voice notes deterministically, no model. It lists `#pontos/raw` and `#pontos/silver` with one `rclone lsjson --recursive` each, downloads only the classification siblings and the .html notes to a temporary folder, and checks every `HHMM-voice-*-classification.md`: the YAML front matter parses (an unquoted `#462` is a comment, or a parse error in a list), the exact key set, the enums of `project`, `type`, `tone` and `confidence`, `topics` among the slugs of `topics.yaml`, `source` is this sibling's existing raw note, `day` is the day folder, `time` is the `HH:MM` of the file name (null for `0000-`), and `issue_refs` are `#123` or github.com issue and pull request URLs, never a CSS colour of the note (`#111`). It also checks coverage (every voice note has its sibling, `<prefix>-<ext>-classification.md` for non-.md notes; a note newer than the last watermark is pending, not missing), siblings with no note, and duplicate folders or files (Drive allows two with the same name).

Errors make it exit 1. For review, not errors: project `other`, no topics, confidence low, and a project other than the majority project of its topics in `topics.yaml`. For information only: classifications from before 2026-11-08 with an old `source:` path (`dump-mental-prompts/sessions/...`), whose old schema is not counted as errors, and siblings of non-.md notes still under the old name `<prefix>-classification.md`. The report goes to `#pontos/silver/classification/<today>/NN-check-report.md`, the next free `NN` of the day's run files, and ends with a `flagged:` YAML list of the paths for the reviewer. A classification flagged only for review leaves that list once `classification-grades.jsonl` holds a grade for it with the same `classified_at` and that grade is not `wrong` (a `grader: silvio` line wins); it comes back when the classification changes, and errors are always flagged; `--dry-run` prints it instead, `--remote` (env `PONTOS_REMOTE`) changes the remote. The systemd user timer `pontos-classification-check.timer` runs it daily at 05:30 local (`Persistent=true`), after the classification run; `scripts/utilities/pontos/install.sh` installs and enables it, running the script from the main clone `~/git/linux`.

`pontos-extract-refs` is the fixed part of the classification: a single Python file with only the standard library and no rclone, so the cloud classification routine runs it in its sandbox from `#pontos/silver/classification/tools/pontos-extract-refs.py`. It reads note files and prints one JSON line per file with `to_refs` (order ids `YYYYMMDD-HHMM` and note file names `*.md`, `*.html`, without fragments), `issue_refs` (`#123` outside CSS: `<style>` blocks, `style=` attributes, CSS rules and colour declarations, colours in attribute values; plus github.com issue and pull request URLs) and `source_urls` (http(s) URLs, deduplicated, trailing punctuation stripped). An .html note loses its `<style>` and `<script>` blocks and its tags first; the links of its `href` and `src` attributes count as `source_urls`. After a change, publish it again: `rclone copyto scripts/bin/pontos-extract-refs 'gdrive:#pontos/silver/classification/tools/pontos-extract-refs.py'`.

## Opt-in and privacy

Only repositories of `smsilva`, `getnereus` and `wasp-foundry` are saved; another one only when listed in `claude/pontos/allow-list` (public: only names that may be public) or `~/.config/pontos/allow-list` (local). Client and employer work never reaches the Drive.

Before any upload, the check refuses secrets (tokens, keys, kubeconfig and cloud credentials, the live value of any secret in the environment), personal data (CPF, phone numbers, street addresses, e-mails other than `example.com` and the repository's own `git config user.email`) and the names in `~/.config/pontos/deny-list`.

## Blocked logs

A blocked or failed file stays in the spool, the status line shows `⚠ pontos`, and the next session starts with a warning.

**Redact.** `pontos-save redact --session <id 8>` (one session at a time) replaces the whole line of a secret with `[REDACTED]`, and an e-mail, a live value or a denied name in place (in that session's later builds too), and uploads; `--dry-run` counts first. It stays blocked when the redact replaced nothing, when a live value is one this environment's variable does not hold, or when a hidden line leaves a value's own quote open, has quotes not in pairs, holds an escaped quote (`\\'`, `\\"`) or ends in a backslash (its value may go on in the next lines; an apostrophe counts too). A value that ends on its line (its own quote closed, then a space, a delimiter or the line's end) clears when only a wrapper stays open, a Python `'''` string or a shell `\` continuation: the quotes of the code block it sits in pair (an apostrophe inside a word aside), or, outside a block, they pair within the next 200 lines of its turn, with no secret joined across the lines. Then run it from the session that was blocked, or leave it for the owner.

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
