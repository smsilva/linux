# Deterministic

The owner's pillar for every repository (2026-10-29): **always pursue the deterministic.**

- The good-enough version may start probabilistic, an agent doing the work by following a rule; that is fine as a first step.
- The solution then evolves toward a deterministic one: a script, a hook, a test or a check that does the same every time, with AI kept only where judgement is needed (a summary, a classification, an extraction).
- It joins the open-source-first pillar: before building, look for a ready open-source solution, and prefer a deterministic one even when the first version is probabilistic.
- When a rule depends on an agent remembering it, propose the hook or check that enforces it. Example: `claude-guard-main-clone` blocks a change in a main clone instead of trusting the agent to remember the worktree rule; Pontos's hooks write the raw log instead of the agent.
