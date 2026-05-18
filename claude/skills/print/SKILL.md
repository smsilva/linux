---
name: print
description: Read the last screenshot from ~/Pictures/screenshots/, or take a new one. Use when the user says "olha o print", "veja o print", "tirar print", "capturar tela", or shares a screenshot they just took.
---

## Screenshot directory

`~/Pictures/screenshots/`

Files are named `YYYY-MM-DD_HH-MM[_N].png` — created by GNOME Screenshot or the Print Screen key.

## Workflow

### Mode A — Read the latest existing screenshot (default)

```bash
ls -t ~/Pictures/screenshots/*.png | head -1
```

Read the returned path with the `Read` tool. Describe what you see and continue with the task.

### Mode B — Take a new screenshot

Use only when the user explicitly asks to capture the screen now.

```bash
scrot ~/Pictures/screenshots/"$(date '+%Y-%m-%d_%H-%M')".png
```

Then read the captured file with the `Read` tool.

#### Installing scrot

```bash
sudo apt install --yes scrot
```

## Notes

- Always open the image with the `Read` tool, not just print the path.
- If the user refers to a specific screenshot (e.g. "the 08:37 one"), find the closest match by timestamp.
- Do NOT use `peek` for this — `peek` is for mid-task UI verification with multi-monitor support.