---
name: remote-session
description: Use when the owner asks for a new remote Claude session ("cria uma nova sessão remota", "abre outra sessão do Claude com remote control", "nova sessão remota", "new remote session"), to drive it from the phone or claude.ai/code. Opens a new tmux window, starts `agent` in it and turns on `/remote-control`, through the `claude-remote-session` script.
---

# New remote Claude session

The owner works from the phone through the Claude app and wants more sessions to drive from there. One script does every step the same way each time (the deterministic pillar):

```bash
claude-remote-session \
  --directory "<folder>" \
  --name "<window name>"
```

It opens a new tmux window in that folder, runs `agent` (Claude Code with bypass permissions), waits for its prompt, sends `/remote-control` (pressing Enter again if the command menu takes the first one), waits for "remote-control is active" and prints:

```text
window: 0:3 pane: %41
url: https://claude.ai/code/session_<id>
```

## Steps

1. **Folder:** the one the owner names; otherwise the current session's working directory. `--name` only when the owner gives one.
2. **Run** the script and read what it prints.
3. **Report** in pt-BR: the window and pane, the URL, and that the session shows up in the Claude app. The new session has no prompt yet: send it one only when the owner asks (`tmux send-keys -t <pane> -l '<text>'`, then `Enter`).
4. **On failure** (Claude Code did not start, Remote Control did not turn on): show the last lines of the pane (`tmux capture-pane -p -t <pane> | tail -20`) and say what failed; leave the window open for the owner to look at.

## Notes

- Needs a running tmux server; the window opens in the current tmux session.
- `agent` is `~/.scripts/agent`; the script adds nothing to it, so its tips and options stay the same.
- The new session is a peer: coordinate with it as with any other session on the same repository (the repository's own rules, such as Nereus's `room` skill).
