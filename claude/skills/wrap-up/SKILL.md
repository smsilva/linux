---
name: wrap-up
description: Use before /clear or at the end of a session, when the owner asks what is worth keeping ("antes do clear", "o que guardar", "veja se temos o que guardar em issues", "fechar a sessão", "encerrar", "wrap-up"). Gathers the repository's facts with `wrap-up-facts`, sweeps the conversation for loose ends, and proposes one numbered table of where each one goes (issue, handoff, rule, owner action); acts only on the owner's go, writes the Pontos notes (the agent's own part) without asking, delegating to the issue, handoff and save-session-learnings skills.
---

# Wrap up a session

Nothing of value may stay only in the conversation: what was decided, found or left for later goes somewhere durable before `/clear`. This skill proposes first and acts only on the owner's go; the proposal is the dry run. The Pontos notes are the exception: they are the agent's own part (`pontos.md`), so they are written without asking and shown in the report.

## Rules

- Never push, merge, claim, release or delete anything here. Leftover worktrees and branches are reported, not proposed for cleanup (cleanup has its own rule in `workflow.md`).
- More than ten items In Progress for the owner on the board: say so and ask which ones stay (`wip.md`).
- Pontos: read its status and write the notes (title, summary, decisions) without putting them in the proposal; a blocked file gets `pontos-save redact` at once, without asking, and the owner hears about it afterwards (`pontos.md`).
- Delegate instead of repeating: an issue goes through the project's `issue` skill (else plain `gh issue create`), a handoff through the project's handoff skill (`<project>-handoff`, such as `nereus-handoff`, or a project `handoff`), else the global `handoff`, a learning through `save-session-learnings`, a Pontos note through `pontos-save note`.

## Steps

1. **Facts.** Run `wrap-up-facts` (add `--json` when parsing) from the repository. Show nothing yet. A source reading `unavailable` is a fact too: no board, no `gh`, not a repository. Inside Claude Code it reads this session's tool calls (`$CLAUDE_CODE_SESSION_ID`) and marks each worktree, board item and issue `this session` or `another session`, since every session shares one `gh` account: only `this session` items are yours to propose; the others are reported in one line and left alone.

2. **Sweep the conversation** for:
   - loose ends: work started and not finished, a step skipped, a check not run;
   - decisions taken (who, when) not yet written in an issue, ADR or doc;
   - review or security findings only acknowledged, without a fix or an issue;
   - "later", "depois", "fica para outra" items, and roadmap steps without an issue;
   - the owner's corrections of how the agent works (a rule or a learning);
   - from the facts: uncommitted changes, branches not pushed, open PRs, merged worktrees still on disk, Pontos logs not on Drive.

3. **Route each item** to one destination:
   - `issue` (new, sub-issue, or comment on an existing one: search first);
   - `handoff` (a comment on the In Progress issue: last step, next step, open decision);
   - `regra` (a rule file or `CLAUDE.md` note);
   - `pontos` (title, summary with `Radar:` lines, decisions): never in the table, written in step 6;
   - `owner` (something only the owner can do: a login, a merge, a cleanup);
   - `nada` (already recorded: say where, e.g. "#505 (agent login renewal)").

4. **Issues first.** Open the proposal with the `issues` facts in a table (`| Papel | Issue | Estado |`), one row per issue with its number and title:
   - **Atual:** the issue In Progress, or the one(s) closed in this session (of those `closed today`, name only the ones this conversation closed), saying which;
   - **Sequência:** the open issues that follow it (`then:`);
   - **Próxima depois do `/clear`:** what `queue next` gives;
   - when the facts say `warning: the next issue is held by another session`, say it in bold: `/next` alone would take that session's issue, so name the number to pass (`/next <n>`) or `--new`;
   - when the facts say `warning: the next issue does not follow the sequence`, say it in bold, name the issue of the sequence that should come next, and propose an item that reorders the board (`scripts/board/queue status <n> Todo` and `move <n> --top`), so `/next` resumes the sequence.

5. **Propose** in pt-BR, in the colors of `communication.md` (🟢, then 🟠, then 🔴, numbered across the colors, ending with the weighing of each 🔴), each item with its destination and proposed text, so the owner can answer by voice or phone. Facts that need nothing go in the 🟢 line (e.g. "3 worktrees mergeadas no disco: limpeza fica com você"). Without a board or a project `issue` skill, propose plain `gh`; without a remote, only `HANDOFF.local.md`.

6. **Act** once every 🔴 is answered, on the approved items only (a 🟠 the owner did not mention counts as approved), and write the Pontos notes (`pontos-save note title|summary|decisions`) whatever the answer. Each action stands alone: report a failure and go on with the next.

7. **Report** what went where (the Pontos notes included), every issue and PR number with its short description, then "pronto para `/clear`" (and `/next` in a repository with a board, naming the issue it will pick). In the main session, `speak` one short pt-BR sentence with the outcome when the project asks for it.
