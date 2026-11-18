---
name: push
description: Use when the owner asks to be told by push notification when the work ends ("avise com push notification quando terminar", "me avisa por push", "manda um push quando acabar", "notifica quando terminar", "/push", "push me when it's done"). Makes this session send one `PushNotification` when what is running now finishes or stops on something that needs the owner, so the owner can leave the screen.
---

# Push when done

The owner is leaving the screen and wants one push notification on the phone when the work in hand ends. This skill is that order: it changes nothing in the work itself.

## Steps

1. **Fix what "done" means.** With an argument (`/push when the checks pass`), that is the condition. With none, it is the task in hand, at the point the owner has something to read or decide: the whole task, not its next step (the checks ending is not "done" when the commit and the PR description still follow).
2. **Confirm in one line** in pt-BR what will trigger the push, then keep working. Never stop to wait for an answer to that line.
3. **Send exactly one `PushNotification`** (load it with `ToolSearch` `select:PushNotification` when it is deferred) at the first of:
   - the work is done and verified;
   - the work failed and cannot go on without the owner;
   - a decision, an approval or a `/ship` is needed before the next step.
4. **Write the message** as one line under 200 characters, in pt-BR, no markdown, leading with what the owner must do or know, then the outcome. Name an issue or a PR with its short description, never a bare number.

   ```text
   /ship? #1676 (--version e --examples recusam o que o Click recusa): make checks passou, PR pronto
   make checks falhou em lint (2 erros) na #1676 (--version e --examples recusam o que o Click recusa)
   ```

5. **Then write the full answer in the chat** as usual: the push only brings the owner back, the detail is in the session.

## Rules

- One push per order: no pushes for progress, and none for a step that ends while the task goes on. A new order (`/push` again) is a new push.
- A "not sent" result means the owner is at the terminal or notifications are off: say nothing about it and go on.
- The order holds across background runs: when a background command or agent is what the task waits for, send the push in the turn its notification arrives and the rest of the task is finished.
- Only the main session sends it; a subagent or a workflow reports to its session, which pushes.
- `/ship push` is this order chained after `ship`: the push comes when `ship` ends, merged or stopped (`claude/skills/ship/SKILL.md`, "Options").
- It adds to the anchored-session rule of `claude/rules/communication.md` (a push whenever a task ends on something the owner must answer); it never replaces it.
