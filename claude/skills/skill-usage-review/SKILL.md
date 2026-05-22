---
name: skill-usage-review
description: Use after a task that involved a skill to improve it based on what just happened — triggered by "can we improve this skill?", "update the skill to handle this automatically", or "enhance the skill"
---

## Steps

1. **Identify the skill that was used** — find the most recent skill invocation in the conversation (look for `Skill` tool calls or `/skill-name` commands). Review the back-and-forth to identify what the user had to correct or add manually.

2. **Read the skill** — read `~/.claude/skills/{name}/SKILL.md` to understand what it already instructs.

3. **Analyse the back-and-forth after invocation** — look for:
   - Corrections the user had to make ("actually, do it like this")
   - Follow-up requests that logically belong inside the skill's workflow
   - Steps Claude performed manually that could be encoded as instructions
   - Approval prompts that could be replaced by a sensible default

4. **Draft improvements** — for each gap, propose a new instruction or a default behaviour change.

5. **Present to the user** — show proposed changes in diff format with a one-line rationale each. Ask for approval before editing.

6. **Apply approved changes** — edit `SKILL.md` using the Edit tool.
