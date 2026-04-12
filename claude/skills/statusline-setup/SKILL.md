---
name: statusline-setup
description: Use this skill to configure the Claude Code status line setting. Invoked when the user asks to change, fix, or add something to the statusline.
---

# statusline-setup skill

Configure and update the Claude Code statusline displayed at the bottom of the terminal.

## File locations

There are two copies that must always be kept in sync:

| File | Role |
|------|------|
| `~/.claude/statusline.sh` | Active — executed by Claude Code via `settings.json` |
| `~/git/linux/scripts/bin/claude-status-line` | Source of truth in the git repo |

Edit both files on every change. The linter/autosave in the IDE often syncs the repo file automatically — always verify after editing `~/.claude/statusline.sh`.

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

The script receives a JSON payload on stdin with fields including:
- `.workspace.current_dir` — current directory
- `.workspace.project_dir` — git root
- `.context_window.used_percentage` — float, e.g. `33.4`
- `.model.display_name` — e.g. `Claude Sonnet 4.5`

## Segment layout

```
[ location ] ▶ [ branch  git-indicators ] ▶ [ ≡ ctx% ] ▶ [ ◔ time ] ▶ [ model ] ▶
    bg=31           bg=236                    bg=dynamic    bg=dynamic    bg=238
```

### Powerline separator pattern

Each separator uses `fg=left_bg, bg=right_bg` to create the filled-triangle transition:

```bash
printf "\033[38;5;<LEFT>m\033[48;5;<RIGHT>m%s"  "$sep"   # LEFT → RIGHT
```

`sep=$'\ue0b0'` — powerline right-pointing filled triangle (requires Nerd Font).

### Fixed segment backgrounds (256-color)

```bash
section_location_background_color=31   # dark blue
section_branch_background_color=236    # #303030
section_model_background_color=238     # #444444
```

Text on dark segments uses `\033[38;5;247m` (light gray) or `\033[38;5;0m` (black).

## Dynamic segment: context % (seg 3)

Thresholds defined as constants at the top of the script:

```bash
ctx_threshold_critical=85
ctx_threshold_warning=60
```

```bash
if   [ "$used_int" -ge "${ctx_threshold_critical}" ]; then section_ctx_background_color=1; section_ctx_foreground_color='\033[30m'
elif [ "$used_int" -ge "${ctx_threshold_warning}" ];  then section_ctx_background_color=3; section_ctx_foreground_color='\033[30m'
else                                                       section_ctx_background_color=2; section_ctx_foreground_color='\033[30m'
fi
```

Rendered as `≡ 33%` — percentage with the `≡` symbol (U+2261).

## Dynamic segment: session time (seg 4)

Thresholds defined as constants at the top of the script (in seconds using `$(( ... ))`):

```bash
time_threshold_critical=$(( 60 * 60 )) # 60 minutes
time_threshold_warning=$(( 30 * 60 ))  # 30 minutes
time_threshold_caution=$(( 15 * 60 ))  # 15 minutes
```

```bash
if   [ "$elapsed_sec" -ge "${time_threshold_critical}" ]; then section_time_background_color=88;  section_time_foreground_color='\033[38;5;15m'  # white on bordeaux
elif [ "$elapsed_sec" -ge "${time_threshold_warning}" ];  then section_time_background_color=215; section_time_foreground_color='\033[30m'        # black on orange
elif [ "$elapsed_sec" -ge "${time_threshold_caution}" ];  then section_time_background_color=221; section_time_foreground_color='\033[30m'        # black on amber
else                                                           section_time_background_color=114; section_time_foreground_color='\033[30m'        # black on green
fi
```

Rendered as `◔ 5m` — circle symbol (U+25D4) followed by the human-readable uptime.

### VS Code minimum contrast ratio

VS Code enforces a minimum contrast ratio of 4.5 by default (`terminal.integrated.minimumContrastRatio`). When a background color is too light, VS Code automatically overrides the foreground color — white text on a light background will silently become dark text.

**Rule:** foreground color must have contrast ratio > 4.5 against its background, or VS Code overrides it.

- `\033[30m` (black) on any bright/pastel background: always passes ✓
- `\033[38;5;15m` (white) requires background luminance < 0.18 — only dark colors qualify (e.g. bordeaux 88 RGB 135/0/0 gives ~8.7:1 ✓; salmon 203 RGB 255/95/95 gave ~2.4:1 ✗)

## External tools used

| Tool | Purpose |
|------|---------|
| `git-status-indicators` | Produces colored dirty/clean git symbols; `--bg <branch_bg>` restores segment bg after each reset |
| `process-uptime` | Returns session duration; `--name claude --format human` for display, `--format seconds` for threshold math |

## Adding a new segment

1. Pick a background color number
2. Add content printf: `printf "\033[48;5;<N>m\033[38;5;0m %s " "$value"`
3. Add separator before: `printf "\033[38;5;<PREV>m\033[48;5;<N>m%s" "$sep"`
4. Add separator after: `printf "\033[38;5;<N>m\033[48;5;<NEXT>m%s" "$sep"`
5. Add a named variable for the background: `section_<name>_background_color=<N>`
6. Sync both files
