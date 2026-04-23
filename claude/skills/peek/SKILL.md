---
name: peek
description: Get visual feedback from the user's screen using scrot. Use this skill whenever you need to see what is on the user's screen and cannot automate the action yourself — e.g. to verify a UI state, inspect a running process, or confirm a visual result.
---

## Screenshot path

Format: `/tmp/peek/<topic>/<seq>_<description>.png`

- **topic** — short slug for the current task (e.g. `e2e`, `login-flow`)
- **seq** — zero-padded 3-digit counter, auto-incremented within the topic directory
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

Announce the full path(s) to the user **before** taking any screenshot. Tell the user:
- What action to perform or what to have on screen
- The exact path(s) where screenshots will be saved
- To return to the terminal and confirm when ready

Wait for confirmation before proceeding — unless the user mentions "other screen" or "second monitor".

### 2. Detect monitors

After the user confirms (or mentions multiple monitors), run:

```bash
xrandr --query | grep ' connected'
```

Each geometry is `WxH+X+Y`. Convert to scrot's `-a X,Y,W,H` format when targeting a specific monitor.

### 3. Capture

**Single monitor:**
```bash
scrot "${peek_path}"
```

**Multiple monitors** — capture one screenshot per monitor:
```bash
scrot -a 0,0,1920,1080 "${peek_dir}/${peek_seq}_<description>_screen1.png"
scrot -a 1920,0,2560,1440 "${peek_dir}/${peek_seq}_<description>_screen2.png"
```

Use `--delay 3` only when the user needs time to switch focus first.

> `--geometry` is not supported on all scrot versions; always use `-a X,Y,W,H`.

### 4. Open and read

Open every screenshot in VS Code, then use the `Read` tool to inspect each image visually.

```bash
code "${peek_path}"
```

If multiple monitors were captured, tell the user which screens were found and guess which one they're likely looking at based on content.

### 5. Continue

Describe what you see and proceed with the task. For subsequent captures, skip monitor detection — reuse the same monitor and increment the sequence counter.

## Installing scrot

```bash
sudo apt install --yes scrot
```
