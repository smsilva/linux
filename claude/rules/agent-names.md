# Agent names

The owner's rule for every repository (2026-10-31): **every agent session on this machine has a unique name from the NATO phonetic alphabet**, lowercase, in the ICAO spelling: alfa, bravo, charlie, delta, echo, foxtrot, golf, hotel, india, juliett, kilo, lima, mike, november, oscar, papa, quebec, romeo, sierra, tango, uniform, victor, whiskey, x-ray, yankee, zulu; after zulu, `alfa-2`, `bravo-2` and so on.

- **The hooks give it, not the agent:** `SessionStart` runs `nato-name hook`, which takes the first free name (atomically, under `flock`, in `~/.local/state/nato-names/`, one file per name) and puts "Your name is <name>" in the session's context; `SessionEnd` frees it. A name whose process is gone (a crash, a kill) is taken again by the next session. `/clear` keeps the name.
- **The launcher shows it:** `agent` reserves the name before Claude Code starts and passes it as `--name`, so other sessions see it in `ListAgents` and the owner sees it in the session list.
- **Know it and say it:** when the owner asks your name, answer with it. Sign cross-session messages, orders and replies with it when relevant. A subagent has no name of its own: it works under its session's.
- **Look it up:** `nato-name whoami --session-id <id>`; `nato-name list` shows every name in use, its session, pid and whether it is still alive.
- A repository's own naming rule for sessions (a tmux window name) gives way to this one.
