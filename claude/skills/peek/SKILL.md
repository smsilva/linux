---
name: peek
description: Get visual feedback from the user's screen using scrot. Use this skill whenever you need to see what is on the user's screen and cannot automate the action yourself — e.g. to verify a UI state, inspect a running process, or confirm a visual result.
---

# peek skill

Capture the user's screen to get visual feedback when automated inspection is not possible.

## Screenshot path

Format: `/tmp/peek/<topic>/<seq>_<description>.png`

- **topic** — short slug for the current task (e.g. `e2e`, `argo-deploy`, `login-flow`)
- **seq** — zero-padded 3-digit counter that auto-increments within the topic directory
- **description** — snake_case summary of what is being captured

```bash
peek_topic="e2e"
peek_dir="/tmp/peek/${peek_topic}"
mkdir --parents "${peek_dir}"
peek_seq=$(printf "%03d" $(( $(ls "${peek_dir}"/*.png 2>/dev/null | wc --lines) + 1 )))
peek_path="${peek_dir}/${peek_seq}_<description>.png"
```

## Workflow

### 1. Prepare

Derive `peek_topic`, `peek_seq`, and `peek_path` using the snippet above. Announce the full path(s) to the user **before** taking any screenshot so they know what to expect.

Tell the user:
- What action to perform or what to have on screen
- The exact path(s) where screenshots will be saved
- To return to the terminal and confirm when ready

Wait for the user's confirmation before proceeding.

### 2. Detect monitors

After the user confirms, discover connected displays:

```bash
xrandr --query | grep ' connected'
```

Example output:
```
eDP-1 connected primary 1920x1080+0+0 ...
HDMI-1 connected 2560x1440+1920+0 ...
```

Each geometry is `WxH+X+Y`. Convert to scrot's `-a X,Y,W,H` format when targeting a specific monitor.

### 3. Capture

**Single monitor:**
```bash
scrot "${peek_path}"
```

**Multiple monitors** — capture each one into a separate file:
```bash
# Screen 1 (eDP-1): 1920x1080 at offset 0,0
scrot -a 0,0,1920,1080 "${peek_dir}/${peek_seq}_<description>_screen1.png"

# Screen 2 (HDMI-1): 2560x1440 at offset 1920,0
scrot -a 1920,0,2560,1440 "${peek_dir}/${peek_seq}_<description>_screen2.png"
```

Use `--delay 3` only when the user needs time to switch focus before the shot fires.

> Note: `--geometry` is not supported on all scrot versions. Always use `-a X,Y,W,H` for targeted captures.

### 4. Open and read

Immediately after capturing, open every screenshot in VS Code so the user can see it too:

```bash
code "${peek_path}"
# or, for multiple:
code "${peek_dir}/${peek_seq}_<description>_screen1.png"
code "${peek_dir}/${peek_seq}_<description>_screen2.png"
```

Then use the `Read` tool to load each image and inspect it visually.

**If multiple monitors were captured:** tell the user which screens were found (e.g. "Screen 1: eDP-1 1920×1080, Screen 2: HDMI-1 2560×1440") and ask which one has what they want to show. Continue with the chosen image only.

### 5. Continue

Describe what you see and proceed with the task.

For subsequent captures in the same session, skip monitor detection — reuse the same monitor geometry already identified and increment the sequence counter.

## Installing scrot

```bash
sudo apt install --yes scrot
```

## Example prompt to user

> Please **[action to perform]**.  
> When the screen looks right, come back here and tell me you're ready.  
> Screenshot will be saved to: `/tmp/peek/subject/001_description.png`
