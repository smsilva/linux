---
name: wrap-up
description: Use before /clear or at the end of a session, when the owner asks what is worth keeping ("antes do clear", "o que guardar", "veja se temos o que guardar em issues", "fechar a sessão", "encerrar", "wrap-up"). Gathers the repository's facts with `wrap-up-facts`, sweeps the conversation for loose ends, and proposes one numbered table of where each one goes (issue, handoff, rule, Pontos notes, owner action); acts only on the owner's go, delegating to the issue, handoff and save-session-learnings skills.
---

# Wrap up a session

Nothing of value may stay only in the conversation: what was decided, found or left for later goes somewhere durable before `/clear`. This skill proposes first and acts only on the owner's go; the proposal is the dry run.

## Rules

- Never push, merge, claim, release or delete anything here. Leftover worktrees and branches are reported, not proposed for cleanup (cleanup has its own rule in `workflow.md`).
- More than one item In Progress for the owner on the board: say so and ask which one stays (`wip.md`).
- Pontos: read its status and write the notes only; `pontos-save redact` only on the owner's word (`pontos.md`).
- Delegate instead of repeating: an issue goes through the project's `issue` skill (else plain `gh issue create`), a handoff through the `handoff` skill (the project's, else the global one), a learning through `save-session-learnings`, a Pontos note through `pontos-save note`.

## Steps

1. **Facts.** Run `wrap-up-facts` (add `--json` when parsing) from the repository. Show nothing yet. A source reading `unavailable` is a fact too: no board, no `gh`, not a repository.

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
   - `pontos` (title, summary with `Radar:` lines, decisions);
   - `owner` (something only the owner can do: a login, a merge, a cleanup);
   - `nada` (already recorded: say where, e.g. "#505 (agent login renewal)").

4. **Propose** one numbered table in pt-BR, so the owner can answer by voice or phone ("1, 3 e 5", "tudo", "nenhum"):

   | # | Item | Destino | Texto proposto |
   | --- | --- | --- | --- |

   Below it, one line on the facts that need nothing (e.g. "3 worktrees mergeadas no disco: limpeza fica com você"). Without a board or a project `issue` skill, propose plain `gh`; without a remote, only `HANDOFF.local.md` and the Pontos notes.

5. **Act** on the approved items only. Each action stands alone: report a failure and go on with the next.

6. **Report** what went where, every issue and PR number with its short description, then "pronto para `/clear`" (and `/next` in a repository with a board). In the main session, `speak` one short pt-BR sentence with the outcome when the project asks for it.
