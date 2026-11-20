---
name: statusline-setup
description: Use this skill to configure the Claude Code status line setting. Invoked when the user asks to change, fix, or add something to the statusline.
---

# statusline-setup skill

Configure and update the Claude Code statusline displayed at the bottom of the terminal.

## File locations & sync

Edit `~/git/linux/scripts/bin/claude-status-line`. `~/.claude/statusline.sh` is a symlink to it (created by `install.sh`), so there is nothing to copy.

## settings.json wiring

`~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash /home/silvios/.claude/statusline.sh",
    "refreshInterval": 5
  }
}
```

The script reads a JSON payload from stdin. Fields used, with their fallback defaults:

| jq path | Default | Used for |
|---------|---------|----------|
| `.workspace.current_dir` | `""` | location display, fallback git root |
| `.workspace.project_dir` | `""` | git root, repo name |
| `.context_window.total_input_tokens` | `0` | context tokens and their share of `CLAUDE_CONTEXT_TOKENS_REFERENCE` |
| `.model.display_name` | `"N/A"` | model segment |
| `.rate_limits.five_hour.used_percentage` / `.resets_at` | empty | 5-hour session limit % and reset time (epoch seconds); segment omitted when absent (API-key accounts) |
| `.rate_limits.seven_day.used_percentage` / `.resets_at` | empty | weekly limit % and reset time |

If `.workspace.project_dir` is empty (no git repo), `repo_name` falls back to `basename current_dir` and the branch segment is suppressed.

## Usage limit segments: show or hide

When the owner asks to show or hide the session (5h) or weekly (7d) limit ("deixa só o limite da sessão", "só o semanal", "mostra os dois", "tira os limites"), run the helper; no script edit, takes effect on the next refresh:

| Request | Command |
|---------|---------|
| session only | `claude-status-line-limits --show session` |
| weekly only | `claude-status-line-limits --show weekly` |
| both (default) | `claude-status-line-limits --show both` |
| none | `claude-status-line-limits --show none` |
| current choice | `claude-status-line-limits` |

The choice lives in `${XDG_CONFIG_HOME:-~/.config}/claude-status-line/limits`.

## Pace verdict

The session and weekly segments answer one question: is the pace right, so that neither limit runs out? Each starts with the time left to its reset instead of a fixed `5h` or `7d`, then the usage in white, the reset, and the verdict: an icon and the usage projected at the reset, both in the verdict's color, as in `2h18m 42% ↻ 14:30 • 61%` and `2d12h 59% ↻ Mon 01:00 • 92%` (the label falls back to `5h` or `7d` once the reset has passed).

The two windows have different goals, so each has its own scale:

| Window | Projection at the reset | Verdict | Color | Meaning |
|--------|-------------------------|---------|-------|---------|
| 5 hours | up to 95% | `•` ok | 114 (green) | it lasts until the reset |
| 5 hours | above 95% | `▼` slow | 203 (salmon) | it runs out before the reset: slow down |
| week | below 70% | `▲` push | 39 (blue) | quota will be left over: speed up, with more subagents and parallel sessions |
| week | from 70% to 99% | `•` ok | 114 (green) | keep the pace |
| week | above 99% | `▼` slow | 203 (salmon) | it runs out before the reset: one agent, no subagents, or a day off |

The 5-hour window has no push: using up every 5-hour window would use up the week in under two days. The projection is rounded before the scale applies, so the number and the color never disagree (`• 99%`, `▼ 100%`).

- **5 hours:** `used × 5 hours / elapsed`, computed in the script; none in the window's first 30 minutes, when a few minutes would project far too high.
- **Week:** `claude-usage-forecast --with-percentage` (`used × 7 days / elapsed`); none in the window's first 6 hours.

With the `nereus` CLI installed (getnereus/nereus#1592), the week's projection comes from its cache, `${XDG_STATE_HOME}/nereus/usage/weekly.json` (`figures.forecast`), read with `jq` on every render, and a salmon `!` follows it while `sendFailing` is true. The status line starts `setsid nereus usage report weekly` detached when the reading differs from the cache or the cache is 5 minutes old, at most once a minute; the CLI keeps the same limits, sends to Nereus at most every 5 minutes and backs off on failure. Without `nereus usage`, or before its cache holds the window, `claude-usage-forecast` answers.

Today's goal (`claude-usage-plan --today-goal`) is no longer on the status line; the `UserPromptSubmit` hook (`claude-usage-plan-hook`) still gives it to each session.

## Segment layout

```
[ ⚠ pontos ] ▶ [ location ] ▶ [ branch  git-indicators ] ▶ [ ✦ model ] ▶ [ tokens % ] ▶ [ session left % ↻ verdict % ] ▶ [ week left % ↻ verdict % ] ▶
```

| Seg | Content | Background | Notes |
|-----|---------|------------|-------|
| 0 | `⚠ pontos` | 160 (red) | only when a raw log is not on Drive |
| 1 | `repo/subfolder` | 31 (dark blue) | bold text |
| 2 | `branch  git-status` | 234 (#1c1c1c) | omitted if not a git repo |
| 3 | `✦ Opus 5.5` | 235 (#262626) | model name, gray text |
| 4 | `94k 31%` | 236 (#303030) | context tokens and their share of the reference; only the percentage carries color |
| 5 | `2h18m 42% ↻ 14:30 • 61%` | 237 (#3a3a3a) | 5-hour limit and its verdict; omitted when hidden or absent |
| 6 | `2d12h 59% ↻ Mon 01:00 • 92%` | 238 (#444444) | weekly limit and its verdict; omitted when hidden or absent |

The gray segments lighten one tone at a time from the branch to the weekly limit. Verdicts stay in the text, not in a colored background: a Powerline separator between a gray segment and a colored one leaves a thin colored edge in this font.

## Powerline separator pattern

Each separator uses `fg=left_bg, bg=right_bg` to create the filled-triangle transition:

```bash
sep=$'\ue0b0'  # powerline right-pointing filled triangle (requires Nerd Font)
ansi-text --text "${sep}" --background <RIGHT> --foreground <LEFT>
```

The trailing separator after the last segment resets to no background and is left as an inline `printf`:

```bash
printf "\033[0m\033[38;5;<last_bg>m%s\033[0m" "${sep}"
```

## Dynamic segments

### Context tokens (seg 4)

The percentage is `total_input_tokens` over `CLAUDE_CONTEXT_TOKENS_REFERENCE` (default 300000, set in `scripts/bash_config`): the context a session may reach before a save and `/clear`, not the model's window. The Nereus `UserPromptSubmit` hook (`scripts/metrics/tokens`) reads the same variable for its warning. The percentage text is 114 (green) below `CLAUDE_CONTEXT_THRESHOLD_WARNING` (60), 221 (amber) up to `CLAUDE_CONTEXT_THRESHOLD_CRITICAL` (80), 203 (salmon) from there.

## Branch segment logic

The branch name color signals repo cleanliness:

- `\033[38;5;247m` (gray) — dirty (uncommitted changes / untracked files)
- `\033[38;5;2m` (green) — clean

Both are followed by `\033[0m\033[48;5;${section_branch_background_color}m` to restore the segment background after the reset.

## VS Code contrast rule

VS Code enforces a minimum contrast ratio of 4.5 (`terminal.integrated.minimumContrastRatio`). When the foreground/background contrast is too low, VS Code silently overrides the color.

**Rule when picking a foreground color (use 256-color index):**
- Black (index `0`) on any bright/pastel background → always passes ✓
- White (index `15`) requires background luminance < 0.18 — only very dark colors qualify
  - bordeaux 88 (RGB 135/0/0) → ~8.7:1 ✓
  - salmon 203 (RGB 255/95/95) → ~2.4:1 ✗ (VS Code will override silently)

Always verify new color choices before committing.

## External tools

| Tool | Invocation | Output |
|------|-----------|--------|
| `ansi-text` | `--text <str> --background <N> [--foreground <N>] [--bold]` | Text wrapped in ANSI 256-color escape codes. `--foreground-raw` accepts a full escape sequence instead of an index. |
| `git-status-indicators` | `--dir <git_root> --color --bg <branch_bg>` | Colored dirty/clean git symbols; `--bg` restores segment bg after each ANSI reset inside the string. Empty string if repo is clean. |

All tools must be on `$PATH`. If missing, the script will error and the statusline will be blank.

## Adding a new segment

1. Pick a background color number (256-color palette)
2. **Check VS Code contrast** — use index `0` (black) for text on light/bright backgrounds; index `15` (white) only on dark colors (luminance < 0.18)
3. Add a named variable: `section_<name>_background_color=<N>`
4. Add content: `ansi-text --text " ${value} " --background "${section_<name>_background_color}" --foreground 0`
5. Add separator before: `ansi-text --text "${sep}" --background "${section_<name>_background_color}" --foreground "${section_<prev>_background_color}"`
6. Add separator after: `ansi-text --text "${sep}" --background "${section_<next>_background_color}" --foreground "${section_<name>_background_color}"`
