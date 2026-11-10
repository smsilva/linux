# Agent names

Every agent session on this machine has a unique name from the active lists of names, lowercase (owner, 2026-10-31, lists 2026-11-04). The rule the agents follow is [`claude/rules/agent-names.md`](../rules/agent-names.md); this page is how it works.

## Lists and configuration

The lists live in `lists/`, one file per list: `nereids` (26 Nereids of Hesiod's *Theogony*, active) and `nato` (the NATO phonetic alphabet in the ICAO spelling, off).

`config`, with `~/.config/agent-names/config` on top of it key by key, chooses: `lists` holds the active lists in order; `scope` is `list` (finish one list, then the next) or `all` (one pool); `order` is `listed`, `alphabetical` or `random`. Today: `lists=nereids`, `scope=list`, `order=random`. `agent-name config` shows what is in force.

## The names go round, like hurricane names

Since 2026-11-03, each session takes the next free name of the queue, and a new round is built only when the queue ends, so no name comes back before the whole round has passed, even at random. With every active name in use at once: `ploto-2`, `eudora-2` and so on.

The reference is the Atlantic hurricane names, kept by a World Meteorological Organization (WMO) committee: six lists of 21 names, one per year, recycled every six years; each storm takes the next name, and a season that runs out of names goes on in a supplemental list (the [National Hurricane Center's page](https://www.nhc.noaa.gov/aboutnames.shtml), the [WMO's 2021 decision](https://public.wmo.int/node/20645)). Taken from it: the next name in order, and a second list when the first runs out (the suffix here). Not taken: the rotation here follows the configuration instead of the year, and no name is ever retired. The storms' own names stay out, so no session carries the name of a tragedy.

## Reserved names

`reserved` holds the names that may not be an agent's (the platform's own, and those of Nereus's controllers); a test fails when a list holds one. A controller that takes a name from the myth adds a line there.

## The hooks

`SessionStart` runs `agent-name hook`, which takes the next free name (atomically, under `flock`, in `~/.local/state/agent-names/`, one file per name, `.queue` for the names still to come) and puts "Your name is <name>" in the session's context; `SessionEnd` frees it. A freed name, or one whose process is gone (a crash, a kill), comes back on its turn. `/clear` keeps the name.

`agent-name list` shows every name in use, its session, pid and whether it is still alive. `nato-name` stays as an alias of `agent-name` for the sessions started before the rename.

## The launcher

`agent` reserves the name before Claude Code starts and passes it as `--name`, so other sessions see it in `ListAgents` and the owner sees it in the session list. It also names the tmux window after the session, unless the window was named by hand, and gives the window back to tmux's own name when the session ends. It turns on Remote Control under that name by default (`--local`, `-L`, leaves it off, and so does `AGENT_REMOTE=false` in the environment); `claude-anchored-session` does the same in a new window.
