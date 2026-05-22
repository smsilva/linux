---
name: skill-usage-review
description: Use after finishing a task that involved a skill — when the user asks "can we improve this skill?", "update the skill to handle this automatically", "enhance the skill based on what just happened", or invokes /skill-usage-review
---

## Steps

0. Reviews the recent back-and-forth, identifies what the user had to correct or add manually, and proposes (or implements) targeted improvements to the skill so those steps happen automatically next time.

1. **Identify the skill that was used** — find the most recent skill invocation in the conversation (look for `Skill` tool calls or `/skill-name` commands).

2. **Read the skill** — read the current `SKILL.md` to understand what it already instructs.

3. **Analyse the back-and-forth after invocation** — look for:
   - Corrections the user had to make ("actually, do it like this")
   - Follow-up requests that logically belong inside the skill's workflow
   - Steps Claude performed manually that could be encoded as instructions or bundled scripts
   - Approval prompts that could be replaced by a sensible default

4. **Draft improvements** — for each gap, propose one of: a new instruction, a bundled script, or a default behaviour change.

5. **Present to the user** — show each proposed change as `+ added line` / `- removed line` with a one-line rationale. Ask for approval before editing.

6. **Apply approved changes** — edit `SKILL.md` (and add any scripts) using the Edit tool.
