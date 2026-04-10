---
name: peek
description: Get visual feedback from the user's screen using scrot. Use this skill whenever you need to see what is on the user's screen and cannot automate the action yourself — e.g. to verify a UI state, inspect a running process, or confirm a visual result.
---

# peek skill

Capture the user's screen to get visual feedback when automated inspection is not possible.

## Workflow

1. **Tell the user what to do** — describe the action they need to perform and show the exact path(s) where screenshots will be saved before taking them
2. **Detect monitors** — run `xrandr` to discover connected displays and their geometries
3. **Wait for confirmation** — the user performs the action, positions the screen, returns to the terminal, and says when ready
4. **Take the screenshot(s)** — if one monitor, capture it directly; if multiple, capture each one separately
5. **Ask which screen** — if multiple monitors were found, read all captured images and ask the user which one contains what they want to show
6. **Inspect the result** — read the chosen image with the `Read` tool so you can see it, then **ALWAYS immediately** open it in VS Code with `code <path>` — this is mandatory so the user can also see what was captured

## Screenshot path

Format: `/tmp/peek/<topic>/<seq>_<description>.png`

- **topic** — short slug for the current task or session context (e.g. `e2e`, `argo-deploy`, `login-flow`)
- **seq** — zero-padded 3-digit counter that auto-increments within the topic directory (e.g. `001`, `002`)
- **description** — snake_case summary of what is being captured (e.g. `initial_google_sso_flow_verification`)

```bash
# Derive next sequence number from existing files in the topic dir
peek_topic="e2e"
peek_dir="/tmp/peek/${peek_topic}"
mkdir -p "${peek_dir}"
peek_seq=$(printf "%03d" $(( $(ls "${peek_dir}"/*.png 2>/dev/null | wc -l) + 1 )))
peek_path="${peek_dir}/${peek_seq}_<description>.png"
```

Always announce the full path(s) to the user **before** taking the shot so they know which files to expect.

## Detecting monitors

Run this before taking any screenshot to discover connected displays and their geometries:

```bash
xrandr --query | grep ' connected'
```

Example output:
```
eDP-1 connected primary 1920x1080+0+0 ...
HDMI-1 connected 2560x1440+1920+0 ...
```

Each geometry is in the format `WxH+X+Y` — use these values directly with `scrot --geometry`.

## Installing scrot

If `scrot` is not available, install it with:

```bash
sudo apt install --yes scrot
```

## scrot commands

`--geometry` is not supported on all versions of scrot. Use `-a X,Y,W,H` instead, extracting values from xrandr output (`WxH+X+Y` → `-a X,Y,W,H`):

```bash
# Single monitor — full screen
scrot "${peek_path}"

# Specific monitor by position (from xrandr WxH+X+Y → -a X,Y,W,H)
scrot -a 1920,0,2560,1440 "${peek_path}"

# With a short delay so the user can switch focus
scrot --delay 3 -a 1920,0,2560,1440 "${peek_path}"
```

## Step-by-step for Claude

```
1. Decide what needs to be captured and why.
2. Derive peek_topic, peek_seq, and peek_path as shown above.
3. Tell the user:
   - What action to perform
   - The exact path(s) where screenshots will be saved
   - To return to the terminal and say "ready" when done
4. Wait for the user's confirmation message.
5. Run: xrandr --query | grep ' connected'  to list monitors and geometries.
6. If ONE monitor:
   - Run: scrot "${peek_path}"
   - IMMEDIATELY run: code "${peek_path}"
7. If MULTIPLE monitors:
   - Capture each monitor with its geometry into separate files:
       scrot -a <X,Y,W,H> "${peek_dir}/${peek_seq}_<description>_screen1.png"
       scrot -a <X,Y,W,H> "${peek_dir}/${peek_seq}_<description>_screen2.png"
   - IMMEDIATELY open all captured files in VS Code:
       code "${peek_dir}/${peek_seq}_<description>_screen1.png"
       code "${peek_dir}/${peek_seq}_<description>_screen2.png"
   - Read all captured images with the Read tool.
   - Tell the user which screens were captured (e.g. "Screen 1: eDP-1 1920x1080, Screen 2: HDMI-1 2560x1440").
   - Ask: "Which screen has what you want to show me?"
   - Continue with the chosen image as peek_path.
8. Read the chosen image with the Read tool to analyze it.
9. Describe what you see and continue the task.
```

## Example prompt to user

> Please **[action to perform]**.  
> When the screen looks right, come back here and tell me you're ready.  
> I found 2 monitors — I'll capture both and ask which one to use:  
> - Screen 1 (eDP-1): `/tmp/peek/subject/001_login_page_screen1.png`  
> - Screen 2 (HDMI-1): `/tmp/peek/subject/001_login_page_screen2.png`
