---
name: rollover
description: The owner's manual trigger to carry a session's work over to a fresh remote session ("rollover", "/rollover"). Writes the handoff on the current issue and the Pontos notes without asking, records what needs the owner's go as pending, and opens the next session, unless a decision blocks the next step.
disable-model-invocation: true
---

# Roll a session over to a new one

A session that has grown too long hands its work to a new one and asks the owner nothing: what needs the owner stays on the issue, not in a session waiting for an answer. Unlike `wrap-up`, this skill is not a proposal to approve. It runs only when the owner calls it, while its behaviour is being evaluated.

## Rules

- Never push, merge, claim, release or delete anything, and do not open issues or edit rules: those wait for the owner's go, listed as pending in the comment.
- The issue stays In Progress and assigned: the next session inherits the claim.
- The comment is public by design: name a worktree relative to the repository (`../nereus-826-slug`), never an absolute path, and write no secret, e-mail or personal name.
- After the last step this session starts no more work.

## Steps

1. **The issue.** The number the owner gave; otherwise the issue marked `this session` and in progress in `wrap-up-facts --json`. None, or more than one: stop and say so, since the handoff has nowhere to go.

2. **The generation.** Read the issue's comments for the highest `Rollover <n>`: this one is the next number, starting at 1.

   ```bash
   gh issue view <number> --json comments --jq '.comments[].body | select(startswith("## Rollover"))'
   ```

3. **The sweep.** From the conversation and `wrap-up-facts`: the last step done, the next step, decisions taken and not yet recorded, findings without a fix, "later" items, the owner's corrections, the worktree, branch, uncommitted changes, open PRs and the checks not run.

4. **Blocked or not.** The next session is blocked only when its next step cannot start without the owner's decision. An item the work can go around is pending, not blocking.

5. **The comment.** Write it to a file in the scratchpad and post it with `gh issue comment <number> --body-file <file>`, keeping the printed URL:

   ```markdown
   ## Rollover <n>

   From session `<NATO name>`. Status: continues | blocked.

   **Last step:** ...

   **Next step:** ...

   **State:** worktree, branch, uncommitted changes, PRs, checks not run.

   **Decisions taken:** ...

   **Waiting for the owner's go:**

   - [ ] ...

   **Read only if needed:** a file, ADR or older comment, and what it answers.
   ```

   Aim for about 2000 characters: this comment is the summary the next session starts from, so point to a long text under `Read only if needed` instead of copying it. Leave out a section that has nothing. When blocked, the first box is the blocking decision, marked `Blocks the next step:`.

6. **Pontos.** Write the title, summary and decisions with `pontos-save note title|summary|decisions --file <file>`, then read `pontos-save status`. Never redact: a blocked log stays in the spool and holds back only itself, and what was flagged is the owner's to judge (`pontos.md`). Never name an alert in the issue's comment, which is public.

7. **The next session.** When blocked, skip this step. Otherwise open it in this session's working directory, with one line of prompt:

   ```bash
   claude-remote-session \
     --directory "<this session's working directory>" \
     --prompt "Continue issue #<number> (<title>). Before anything else, read its body (and its parent's body, when it is a sub-issue), its rollover comment <comment URL> and every comment after that one, which may answer or change it. Start at the comment's next step. You take over from session <NATO name>, which does no more work on it; this is rollover <n>. An item waiting for the owner's go stays pending until the owner answers it on the issue."
   ```

   On failure, follow the `remote-session` skill's failure step and say that the handoff is on the issue.

8. **Report** in pt-BR, in a few lines: the issue with its short description, the comment's URL, the status, the items waiting for the owner, the next session's NATO name and URL (`nato-name list`, the newest entry), this session's Pontos alert if any (kind and count, never the value, with `pontos-save redact --session <id 8>` for the owner to run or ask for), and that this session can be closed with `/exit`.
