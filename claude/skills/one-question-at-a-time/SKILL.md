---
name: one-question-at-a-time
description: Use when the owner asks for the open questions one by one ("uma dúvida de cada vez", "uma pergunta por vez", "apresente as dúvidas uma a uma", "me pergunte uma de cada vez", "/one-question-at-a-time", "one question at a time"), or when a design, a triage or a review has several open questions to settle. Presents each question alone, with its context, its options and a recommendation, and lets the owner choose where to answer: the terminal, the visual companion (one browser screen per question) or a deck (one slide per question).
---

# One question at a time

The owner reads from the phone and often follows by voice: a list of questions means scrolling up and down, and an answer to "1, 3 and 5" loses the context of each. This skill makes the session ask one question, wait for its answer, and only then ask the next.

## Steps

1. **Gather the questions first, silently.** List every open question of the work in hand, and drop the ones the request, the code, the docs or a sensible default already answer: those are stated as facts, never asked.
2. **Order them:** a question whose answer changes or removes later ones goes first. Say how many there are in one line ("3 dúvidas").
3. **Ask where to answer, once,** unless the owner already said it or the argument names it (`/one-question-at-a-time deck`). The three surfaces:

   | Surface | What it is | When it fits |
   | --- | --- | --- |
   | terminal | the question in the chat, answered by text or voice | few questions, short options, the owner on the phone |
   | visual companion | one browser screen per question, answered by a click | options worth seeing: a diagram, names, CLI examples side by side |
   | deck | one slide per question in one HTML file, answered in the chat | questions to read away from the session, to keep or to share |

   Recommend one in that question, by the table.
4. **Present one question,** then stop and wait. Each question carries, in this order:
   - its number and the total ("Dúvida 2 de 3");
   - the context in one or two sentences: what was found and why it needs the owner;
   - the options, two to four, each with what it means and what it costs;
   - the recommendation and its reason, in as few words as possible.
5. **After the answer:** confirm it in one line, drop or rewrite the later questions it changed, and present the next. Never present two questions in one message, and never ask the next before the current one is answered.
6. **At the end,** list the decisions taken, one line each, and go on with the work.

## The surfaces

- **Terminal:** `AskUserQuestion` with one question per call, the recommended option first; plain text when the tool is not there. In a repository with the colour format for decisions (🟠, 🔴 in `claude/rules/communication.md`), one item per message.
- **Visual companion:** follow the repository's own rules for companion screens when it has them (Nereus: `docs/agent/owner.md`, "Decisions and spec reviews go through the visual companion"). One screen per question, its content never repeated in the terminal: the reply only says the screen is up, and the click answers it.
- **Deck:** follow the repository's deck rules when it has them (Nereus: `docs/agent/decks.md`, the deck engine). One slide per question, the recommendation on the slide; show the file's absolute path and open it. The owner answers in the chat, still one question at a time: the deck is the reading surface, the order of the answers stays the same.

## Rules

- A question is the owner's to answer only when the answer changes what is done next. A choice with a conventional default is taken and reported, never asked.
- Never gather the recommendations at the end: each sits with its question.
- The owner may answer several at once or say "aceito as recomendações": take that, and skip what it settles.
- A subagent never asks the owner: it returns its open questions to its session, which presents them this way.
