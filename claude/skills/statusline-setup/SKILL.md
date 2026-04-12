---
name: statusline-setup
description: Use this skill to configure the Claude Code status line setting. Invoked when the user asks to change, fix, or add something to the statusline.
---

# statusline-setup skill

Configure and update the Claude Code statusline displayed at the bottom of the terminal.

## File locations & sync

There are two copies that must always be kept in sync:

| File | Role |
|------|------|
| `~/git/linux/scripts/bin/claude-status-line` | Source of truth — edit this first |
| `~/.claude/statusline.sh` | Active copy executed by Claude Code |

**Sync procedure:** Edit the repo file, then copy it verbatim: `cp ~/git/linux/scripts/bin/claude-status-line ~/.claude/statusline.sh`

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
| `.context_window.used_percentage` | `0` | ctx % display and thresholds |
| `.context_window.total_input_tokens` | `0` | total tokens segment (input side) |
| `.context_window.total_output_tokens` | `0` | total tokens segment (output side) |
| `.model.display_name` | `"N/A"` | model segment |

If `.workspace.project_dir` is empty (no git repo), `repo_name` falls back to `basename current_dir` and the branch segment is suppressed.

## Segment layout

```
[ location ] ▶ [ branch  git-indicators ] ▶ [ ≡ ctx% ] ▶ [ ◔ time ] ▶ [ model ] ▶ [ ∑ tokens ] ▶
    bg=31           bg=236                    bg=dynamic    bg=dynamic    bg=238      bg=244
```

| Seg | Content | Background | Notes |
|-----|---------|------------|-------|
| 1 | `repo/subfolder` | 31 (dark blue) | bold text |
| 2 | `branch  git-status` | 236 (#303030) | omitted if not a git repo |
| 3 | `≡ 33%` | dynamic (green/yellow/red) | context window % |
| 4 | `◔ 5m` | dynamic (green/amber/orange/bordeaux) | session uptime |
| 5 | `model name` | 238 (#444444) | gray text |
| 6 | `∑ 15k` | 244 (#808080) | total tokens (input+output), lighter than model |

All exact threshold/color constants live at the top of the script — treat the script as the source of truth, not this document.

## Powerline separator pattern

Each separator uses `fg=left_bg, bg=right_bg` to create the filled-triangle transition:

```bash
sep=$'\ue0b0'  # powerline right-pointing filled triangle (requires Nerd Font)
printf "\033[38;5;<LEFT>m\033[48;5;<RIGHT>m%s" "$sep"
```

The trailing separator after the model segment resets to no background: `\033[0m\033[38;5;<model_bg>m%s\033[0m`.

## Dynamic segments

### Context window % (seg 3)

Three states based on `ctx_threshold_critical` and `ctx_threshold_warning` (see script top). Colors: `2`=green, `3`=yellow, `1`=red. All use black foreground `\033[30m`.

### Session time (seg 4)

Four states based on three thresholds (see script top). Colors and foregrounds:

| State | bg | fg | Visual |
|-------|----|----|--------|
| normal | 114 | black | green |
| caution | 221 | black | amber |
| warning | 215 | black | orange |
| critical | 88 | `\033[38;5;15m` (white) | bordeaux |

White foreground on bordeaux (88) is intentional — black fails contrast on a dark background. See VS Code contrast rule below.

## Branch segment logic

The branch name color signals repo cleanliness:

- `\033[38;5;247m` (gray) — dirty (uncommitted changes / untracked files)
- `\033[38;5;2m` (green) — clean

Both are followed by `\033[0m\033[48;5;${section_branch_background_color}m` to restore the segment background after the reset.

## VS Code contrast rule

VS Code enforces a minimum contrast ratio of 4.5 (`terminal.integrated.minimumContrastRatio`). When the foreground/background contrast is too low, VS Code silently overrides the color.

**Rule when picking a foreground color:**
- Black `\033[30m` on any bright/pastel background → always passes ✓
- White `\033[38;5;15m` requires background luminance < 0.18 — only very dark colors qualify
  - bordeaux 88 (RGB 135/0/0) → ~8.7:1 ✓
  - salmon 203 (RGB 255/95/95) → ~2.4:1 ✗ (VS Code will override silently)

Always verify new color choices before committing.

## External tools

| Tool | Invocation | Output |
|------|-----------|--------|
| `git-status-indicators` | `--dir <git_root> --color --bg <branch_bg>` | Colored dirty/clean git symbols; `--bg` restores segment bg after each ANSI reset inside the string. Empty string if repo is clean. |
| `process-uptime` | `--name claude --format human` | Human-readable string, e.g. `"5m"`, `"1h 2m"` |
| `process-uptime` | `--name claude --format seconds` | Integer string, e.g. `"300"`. Used for threshold comparisons. |

Both tools must be on `$PATH`. If missing, the script will error and the statusline will be blank.

## Adding a new segment

1. Pick a background color number (256-color palette)
2. **Check VS Code contrast** — use black `\033[30m` for text on light/bright backgrounds; white `\033[38;5;15m` only on dark colors (luminance < 0.18)
3. Add a named variable: `section_<name>_background_color=<N>`
4. Add content printf: `printf "\033[48;5;${section_<name>_background_color}m\033[38;5;0m %s " "$value"`
5. Add separator before: `printf "\033[38;5;<PREV_BG>m\033[48;5;${section_<name>_background_color}m%s" "$sep"`
6. Add separator after: `printf "\033[38;5;${section_<name>_background_color}m\033[48;5;<NEXT_BG>m%s" "$sep"`
7. Sync both files (see File locations & sync)
