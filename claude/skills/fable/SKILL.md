---
name: fable
description: Use when the owner asks for a second opinion ("segunda opinião", "pede uma segunda opinião", "pergunta pro fable", "o que o fable acha", "/fable", "second opinion"). Briefs a fresh agent on the Fable model with the question and the checked facts, without this session's recommendation, runs it in the background, and relays where it agrees, where it disagrees and what it adds, next to this session's own view.
argument-hint: "[the question or decision; default: the open decision of the conversation]"
---

# Fable: a second opinion

A second opinion is worth something only when it is not anchored on the first. This skill hands the question to a fresh agent on the Fable model (`claude-fable-5-2`) with the facts and the options, never with this session's pick, and brings back a read the owner can weigh against the session's own.

## Steps

1. **Pick the question.** The argument, when given; otherwise the decision the conversation left open. If neither names one clearly, ask the owner in one line which decision to send.
2. **Write the brief.** The fresh agent knows only what the brief says, so it carries:
   - the repository path and the files or docs worth reading (paths, not pasted contents);
   - the owner's goal and why, in the owner's words where possible;
   - the facts already checked in this session, stated as facts, with what each was checked against;
   - the options on the table, each with its trade-off, in neutral words and in no order of preference;
   - what is already decided by the owner, marked as such, so the agent does not reopen it;
   - the questions: which option it would pick or a better one, the weakest assumption, practices from other teams with a source name, the first slice it would ship;
   - the limits: read-only (no edits, commits, issues, pushes or cross-session messages), the owner's chat language for the answer (pt-BR for this owner), at most ~500 words, disagree where it disagrees.
   Leave out this session's recommendation and its reasons.
3. **Launch it.** `Agent` with `model: "fable"`, `subagent_type: "general-purpose"`, `run_in_background: true`, a 3–5 word description. Tell the owner in one line that it is running, then go on with other work; never predict its answer.
4. **Relay the answer** when the notification arrives, in the owner's chat language:
   - 🟢 where it agrees with this session;
   - 🟠 where it disagrees or adds something, each with this session's honest reply: accept it, or say why not;
   - 🔴 any decision that changed or opened because of it, with a recommendation under each (the owner's `communication.md` format).
   Quote the agent only where its wording matters; never paste the whole answer. Say plainly when it changed this session's recommendation.
5. **Follow-ups** go to the same agent with `SendMessage`, which keeps its context; a new `Agent` call starts fresh.

## Rules

- One agent per question; several questions at once go to separate agents only when they are independent.
- The second opinion is information, never the owner's decision: nothing is built, merged or changed on its account.
- Subagents never speak (`voice.md`).
