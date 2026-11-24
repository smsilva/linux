---
name: hi
description: Use when the owner greets the session and asks what the plan is ("/hi", "hi", "oi, qual o plano?", "qual o plano?", "e aí, o que vem agora?", "what's the plan?"), most often right after `/clear` or on coming back to the screen. Answers in pt-BR with where the work stands, what is next and what waits for the owner, without starting anything.
---

# Hi: what is the plan?

The owner is back and asks the agent for its plan. This skill is a read-only check-in: it says where things stand and stops; nothing on the cloud, no code, no board change before the owner answers.

## Steps

1. **Find the plan, in this order:**
   - the session prompt already in the context (the `SessionStart` hook puts it there after `/clear`); when it says **STALE**, say so first;
   - otherwise `session-prompt show` (or the repository's own `scripts/session/prompt show` when `session-prompt` names it);
   - otherwise the conversation so far, the current branch and worktree (`git status --short`, `git log --oneline -5`) and the issue the session holds.
2. **Check cheaply what the plan depends on** (a file it names still exists, a branch it names is still there), one or two quick commands; never a heavy run.
3. **Answer in pt-BR**, everything else (files, commits) stays in English:
   - greet the owner by name, sign with the agent's name;
   - one or two lines on the focus (the issue with its short description);
   - the colour summary of `claude/rules/communication.md`: 🟢 what is known, 🟠 what the agent will do unless told otherwise, 🔴 each question that waits for the owner, each 🟠 and 🔴 with its `**Recomendação:**` right under it.
4. **Stop and wait** for the owner's answer. In an anchored session, send the `PushNotification` the communication rule asks for.

## Rules

- With no plan anywhere, say so in one line and propose the next step (for example the `next` skill), never invent one.
- Follow the plan's own limits (a slow machine, no subagents, one heavy run at a time) in the answer itself.
- Every issue or PR number carries its short description.
