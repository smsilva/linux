---
name: anchored-session
description: Use when the owner asks for a new anchored Claude session ("cria uma sessão ancorada", "nova sessão ancorada", "abre outra sessão ancorada", "new anchored session") or, by the old phrases, a new remote session ("cria uma nova sessão remota", "nova sessão remota", "abre outra sessão do Claude com remote control", "new remote session"), to drive it from the phone or claude.ai/code. Opens a new tmux window, starts `agent` in it and turns on `/remote-control`, through the `claude-anchored-session` script (`claude-anchored-session` still works).
---

# New anchored Claude session

An **anchored session** runs on the owner's machine in a tmux window and is steered remotely (Remote Control, from the phone or claude.ai/code); it is not a cloud session. The owner works from the phone through the Claude app and wants more anchored sessions to drive from there. One script does every step the same way each time (the deterministic pillar):

```bash
claude-anchored-session \
  --directory "<folder>" \
  --name "<window name>"
```

It opens a new tmux window in that folder, runs `agent` (Claude Code with bypass permissions and Remote Control on), waits for "remote-control is active" and prints:

```text
window: 0:3 pane: %41
url: https://claude.ai/code/session_<id>
```

## Steps

1. **Folder:** the one the owner names; otherwise the current session's working directory. `--name` only when the owner gives one: never derive it from the task (an issue number, a slug). Without it, the window takes the session's name, the one the Claude app shows, so the owner sees one name everywhere.
2. **Run** the script and read what it prints.
3. **Report** in pt-BR: the session's name (`agent-name list`, the newest entry), the window and pane, the URL, and that the session shows up in the Claude app under that name. The new session has no prompt yet: send it one only when the owner asks (`tmux send-keys -t <pane> -l '<text>'`, then `Enter`). A session that must start with a prompt takes `--prompt "<text>"` on the script.
4. **On failure** (Claude Code did not start, Remote Control did not turn on): show the last lines of the pane (`tmux capture-pane -p -t <pane> | tail -20`) and say what failed; leave the window open for the owner to look at.

## Notes

- Needs a running tmux server; the window opens in the current tmux session.
- `agent` is `~/.scripts/agent`; the script adds nothing to it, so its tips and options stay the same.
- The new session is a peer: coordinate with it as with any other session on the same repository (the repository's own rules, such as Nereus's `room` skill).
