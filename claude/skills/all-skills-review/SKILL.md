---
name: all-skills-review
description: Use when asked to review all skills, generate a concise ordered summary of suggestions for improving each skill, and provide an overall assessment of the skills' effectiveness
user-invocable: true
disable-model-invocation: true
---

# 1. Visibility:

- Skills with high risk side effects (deploy, commit, send messages): add `disable-model-invocation: true` so Claude can't auto-fire.
- Skills that are pure background knowledge users would never /run themselves: add `user-invocable: false` to hide from /menu.

# 2. Deterministic vs non-deterministic:

- Find any step inside a skill where AI is interpreting something that's actually a fixed, repeatable operation.
- Suggest replacing those steps with a script saved inside the skill folder.
- Code = same result every time, no token cost. Keep AI for the steps that need judgment.

# 3. Composability:

- Flag any skill that duplicates logic another skill already has.
- Suggest extracting shared logic into a callable script or a smaller composable skill.
- For each duplication found, propose a rewrite and explain what changed and why.
