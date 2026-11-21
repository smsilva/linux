# Session prompt

A session prompt is the instructions a session leaves so the next one, after `/clear`, resumes the same way of working (smsilva/linux#203, ported from getnereus/nereus#1239). It carries no memory of what was done: the work itself is in the repository, the issues and the board. `session-prompt` (`scripts/bin/session-prompt`) keeps it; never write its path by hand.

## The cycle

1. **A session starts:** the global hook (`session-prompt hook`, on every `SessionStart` and `SessionEnd`, `claude/settings.json`) records its start in `<git common dir>/session-prompts/<agent name>.session`.
2. **Before `/clear`:** the agent drafts its prompt (in English, imperative, to a fresh agent: the context, each standing instruction, the start; not what was done) in its scratchpad and runs `session-prompt save --file <draft>`, without asking the owner to confirm. It shows what it saved and only then tells the owner the session can be cleared. The file is `<git common dir>/session-prompts/<agent name>.md` (`session-prompt path` prints it); with `PROMPT_TEAM` set (a command the owner chooses, e.g. a board's team panel), its output goes in a `## Board at save` block; a repository's own scripts never run from here.
3. **After `/clear`:** the session keeps its name, and the hook puts the prompt in its context. A prompt rewritten after the ended session's start says "follow it"; one that was not says **STALE**.
4. **A session that ends for good** (`/exit`, a closed window, not `/clear`): the hook archives the prompt to `~/.claude/prompts/<repository>/<agent name>-<date>.md`, so a later session that gets the name starts clean.
5. **That same session resumed** (`claude --resume <id>`, the command Claude Code prints at exit): the end left `<agent name>.ended` next to the prompt, with the session id, the archive and the session's start; a `SessionStart` with `source=resume` and the same session id moves the archive back, restores the start (so the prompt is not STALE at the next `/clear`) and puts one line in the context, since a resume already carries the conversation (#218). Another session of the same name never takes it.
6. **`session-prompt clear --topic <name>`:** archives the prompt under a topic, once the owner confirms.

## The rules

- **One prompt per agent:** the key is the agent's name (`AGENT_NAME`, set by the `agent` launcher, else `agent-name whoami`), so every worktree of that agent finds the same file and parallel agents never overwrite each other. Outside a named session there is no prompt. A single `HANDOFF.local.md` per repository is the file two agents would collide on.
- **Inside the git folder, not the working tree:** the hook tells the session to follow the prompt, so it must be one this tool wrote. A file in the working tree could have come with the clone, written by the repository's authors; nothing under the git folder ever does, and nothing there is ever committed, so no `.gitignore` line is needed.
- **STALE:** say so to the owner before following it, check its state against the repository, and rewrite it once checked.
- **If the branch or checkout path differs from the prompt's header,** say so and ask before the first commit.
- **Nereus** keeps its own `scripts/session/prompt` until getnereus/nereus#1953; the global hook skips a repository that has one, so the prompt is not printed twice.
- **What the hook cannot do:** write the prompt (that takes judgement) or stop a `/clear`. The rewrite before `/clear` stays the agent's part; STALE shows when it was skipped.
- **Untrusted repositories:** the hook runs in every repository. Besides keeping its files in the git folder, the script refuses symbolic links there, writes through a temporary file, reads the `.session` epoch only when it is all digits, and runs no command of the repository.
