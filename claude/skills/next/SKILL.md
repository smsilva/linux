---
name: next
description: Use when the owner asks to pick up, resume or start the next issue of a repository ("next", "próxima issue", "pegue a próxima issue", "pega uma nova", "o que o time está fazendo"), or names an issue number to work on. The owner types short words (a number, `team`, `save`, `clear`) or free phrases, never flags. Claims the issue, loads its context and presents the design before any implementation. With a session prompt for this agent (`session-prompt show`), follows it instead; "save" writes it from the current session, also when the owner asks for "um prompt para depois do clear" or "salva o prompt da sessão"; "clear" archives it.
argument-hint: "[number | new | team | <field> <value> | save | clear]"
---

# Next issue

The queue is the repository's issues, ordered by its board when it has one. "Me" is the active `gh` account (`gh api user --jq .login`). An issue someone else holds is never mine. This skill loads one issue and stops at a design for the owner to approve.

A repository with its own `next` skill (`.claude/skills/next/`, such as getnereus/nereus until getnereus/nereus#1953) uses that one: it is the more specific.

## The repository's `.claude/next.md`

Each repository says where its queue lives and what a design there must cover, in a versioned `.claude/next.md`: a YAML front matter for the board, a body for the design checklist.

```markdown
---
board: none
---
# Next

A design here covers: the script (bash-scripts rules), its test in scripts/tests/, the doc it changes, and how to try it live before shipping.
```

| `board` | Queue |
| --- | --- |
| `none`, or no `.claude/next.md` | the repository's open issues, through `gh` |
| `github-project` (with `owner`, `number`, `repository`, `fields`) | `board-queue` (`scripts/bin/board-queue`; `board-queue config` prints what it read) |
| `jira` | the `jira-workflow` skill (smsilva/linux#203 task 5) |

Read it before step 1. When `board` names a backend whose tool is not installed (`command -v board-queue` fails), say so and fall back to `none`.

## Session prompt

A session prompt is the instructions a session leaves so the next one, after `/clear`, resumes the same way of working; `session-prompt` keeps one per agent (`~/git/linux/claude/session-prompt/README.md`). Never write its path by hand.

- **No argument:** run `session-prompt show`. With a prompt, follow it in place of the steps below; with none (it exits non-zero), run the steps.
- **After `/clear`:** the `SessionStart` hook already put the prompt in the context: follow it. When it says **STALE**, tell the owner first, check its state against the repository and the issues, and rewrite it with `save` once checked. If the branch or checkout path differs from its header, say so and ask before the first commit.
- **`save`** (also "um prompt para depois do clear", "salva o prompt da sessão"): draft the prompt in the scratchpad (in English, imperative, to a fresh agent: the context, each standing instruction, the start; not what was done), with the date, the branch, the checkout path and the agent's name in the header. When `session-prompt show` prints one, merge into it. Run `session-prompt save --file <draft>` at once, without asking; show what was saved and the path it prints, then say the session can be cleared. Rewrite it this way before every `/clear`: the hook marks it STALE otherwise.
- **`clear`:** show the prompt; after the owner confirms, run `session-prompt clear --topic <topic>` (`<topic>` in lowercase-hyphenated words, e.g. `status-line-pace`) and show the archive path it prints.

## Steps

1. **Pick the issue.**

   - **Coordinate first:** read what the peers hold and are about to take, so two sessions never go for the same issue: `claude-peers` (rows with role `peer`) and the start of each peer's session prompt (`session-prompt show --agent <name>`). Reading sends nothing; skip an issue a peer is about to take and say so. The `room` skill has the protocol.
   - **With a number:** use it, unless `gh issue view <n> --json assignees` shows someone else: then say who holds it and go on only if the owner says it is a takeover.
   - **Without one,** by the board:
     - `none`: list my open issues (`gh issue list --assignee @me --state open`). One: resume it. Several: ask which. None: show the open issues without an assignee (`gh issue list --state open --search "no:assignee" --limit 10`, each with its title) and ask which to take. Never pick one on a guess: without a board there is no order.
     - `github-project`: the owner types a word, you run the command (never the owner the flags):

       | Word | You run |
       | --- | --- |
       | *(none)* | `board-queue next`: my items In Progress, else the top free `Todo` |
       | `<field> <value>` (a field of `fields`, e.g. `track docs`) | `board-queue next --filter <Field>=<value>` |
       | `new` | `board-queue next --new`: one more, while mine stay open |
       | `team` | `board-queue team`: who is on what, claims nothing |

       A value no item has makes `board-queue` print the values in use: ask which one. With an `In Progress without assignee` warning, mention `board-queue doctor` and do not take the orphan. With `Todo` empty, show `board-queue list --status Backlog | head` and ask which to promote. If it fails with `lacks the 'project' scope` or `cannot see board`, relay the fix and stop.
   - **Claim before anything else:** `gh issue edit <n> --add-assignee @me` (with a board: `board-queue claim <n>`, which also sets `In Progress`). A resumed issue of mine needs no claim. Right after the claim, send the `[claim]` to every peer on this repository (the `room` skill).

2. **Read the whole issue.** `gh issue view <n> --comments` omits the body, so run both:

   ```bash
   gh issue view <n> --json title,body,labels --jq '.title, .body'
   gh issue view <n> --comments
   ```

   The last comment is often a handoff (last step, next step, open decision): resume from it. A sub-issue carries only its cut; the scope and acceptance criteria live in the parent (`gh issue view <n> --json parent --jq .parent.number`): read it the same way.

3. **Check the dependencies** the body lists: each one is closed or its code is on `main`. Read **why** each closed one was closed (`gh issue view <dep> --json state,stateReason` and its last comment): one closed as superseded or not planned changes the target. If one is missing, report it and stop.

4. **Check existing work:**

   ```bash
   git branch --all --list "*<n>-*"
   gh pr list --state all --search "<n> in:title"
   ```

   A branch with commits ahead of `main` means resume, not restart.

5. **Read what the issue points to:** the ADRs, specs, docs and code paths it names, and the checklist in `.claude/next.md`. Read before designing: state checked facts, never "verify whether".

6. **Present the design and stop.** Reply in the owner's language with:
   - one line on the issue and its state (new, resuming, blocked), with its short description;
   - with a board, the team panel (`board-queue team`): flag an area shared with someone else as a merge-conflict risk;
   - the usage first: the commands a person types and what they print, or what they see, for each new feature;
   - the cut: one PR, or sub-issues (one per deliverable) when the scope spans several;
   - per deliverable, each item of the `.claude/next.md` checklist;
   - the open points in the owner's colors (`~/.claude/rules/communication.md`): 🟢 information, one line; 🟠 to review, with a suggestion of high confidence; 🔴 the owner's decision. On screen in that order, numbered from the first 🟠 or 🔴, each with its `**Recomendação:**` right under it.

   Write no code, create no branch and change no board before the owner approves.

## After approval

- Create sub-issues when the design splits the work.
- Work in a worktree of its own, on `feat/<n>-<short-description>` from `origin/main` (`~/.claude/rules/workflow.md`).
- Before stopping mid-task, leave a handoff comment on the issue (last step, next step, open decision).
- To give the issue up: `gh issue edit <n> --remove-assignee @me` (with a board: `board-queue release <n>`).
