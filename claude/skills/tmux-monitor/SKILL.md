---
name: tmux-monitor
description: Use when the user mentions a tmux window, pane, or panel — including "what's in that panel", "look at that window" — or asks to monitor a process running in tmux. Do NOT use peek (scrot screenshots) for tmux content — tmux panes are text, not GUI.
---

$ARGUMENTS — `[interval=10] [pane=0:0.1]`

- `interval` — seconds between checks (default: `10`)
- `pane` — tmux pane target in `session:window.pane` format (default: `0:0.1`)

## How it works

Each iteration:
1. Run `sleep <interval> && tmux capture-pane -p -t <pane> -S -60` as a single Bash call (timeout: `<interval> + 20` seconds)
2. Compare output to the previous capture
3. If changed: report what happened in plain text — one short sentence per notable event
4. If unchanged: say nothing, go to next iteration

Repeat until the user interrupts or says to stop.

## Starting

Parse `$ARGUMENTS`. If the pane argument is not provided, run:

```bash
tmux list-panes -a
```

and pick the pane that is NOT the one Claude is running in (i.e. not the active pane of the current window).

Announce once before starting:
> Monitoring pane `<pane>` every `<interval>`s. Interrupt to stop.

Then begin the loop immediately — no further confirmation needed.

## Reporting

- Report only meaningful changes: new commands, output, errors, prompts, status changes
- Skip noise: cursor movement, progress bars updating in place, unchanged content
- Keep each report to 1–2 sentences maximum
- If an error is detected (non-zero exit, error message), flag it explicitly
