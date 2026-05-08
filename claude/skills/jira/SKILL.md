---
name: jira
description: Navigate and work on a Jira issue (epic, story, or task) using the jira-workflow skill
---

Use the `jira-workflow` skill for all Jira operations (MCP, task file, comments, transitions, assignments).

$ARGUMENTS — JIRA_ID (epic, story, or task)

**Paths used in this skill:**
- Project config: `.jira/config.md` (always here)
- Task file: `<jira_folder>/<JIRA_TASK_ID>.md` — read `## Paths` → Jira folder from `config.md`; default `.jira/`

If `.jira/config.md` exists, read it before any action to get project configuration:
site URL, required fields when creating issues, labels, and owner name.
If it doesn't exist, suggest running `/jira-init` to configure the project.

Check `.claude/settings.local.json` for a `PreToolUse` hook calling `validate-task-file.py`. If absent, warn the user that task file writes are unprotected and suggest running `/jira-init` to set it up — then stop.

## Navigation

- If `$ARGUMENTS` is empty:
  - Resolve `<jira_folder>` from `config.md` → `## Paths`; default `.jira/`
  - Look for task files matching `<jira_folder>/*.md` excluding `config.md`
  - If exactly one is found, read it to get the JIRA_ID and context, and continue from where we left off
  - If multiple are found, list them and ask the user to choose
  - If none are found, ask the user for the JIRA_ID
- Fetch the issue by the received JIRA_ID
- If it's an epic: list associated stories that still need work and ask the user to choose one
- If it's a story:
    - list pending tasks and ask the user to choose one
    - if there are no pending tasks, list all tasks with their status and last comment, and ask the user to choose one
- The final working issue must be a task
- Once the task is identified, proceed immediately to **Start task** below — do not wait for further input.

## Start task

> **All operations run in the current working directory** — the directory where `claude` was launched.
>
> Paths mentioned in the issue description (e.g. `~/git/some-project`, `~/git/waspctl`) are **documentation only**. Never use them in any bash command — no `ls`, no `cd`, no `find`, no `mkdir`, no `git init`, nothing. If you find yourself about to run a command with a path from the issue description, stop and drop that command entirely.
>
> Never create a new git repository. If `git status` fails (not a git repo), stop and tell the user.

1. If not assigned, confirm and assign to the current user
2. Create `<jira_folder>/<JIRA_TASK_ID>.md` if it doesn't exist (create the folder if needed; resolve path from `config.md` → `## Paths`, default `.jira/`)
3. If branch `feature/<JIRA_TASK_ID>` **does not exist**:
   - Checkout main and pull latest changes
   - Create branch from main: `git checkout -b feature/<JIRA_TASK_ID>`
4. If branch `feature/<JIRA_TASK_ID>` **already exists** (local or remote):
   - Checkout the branch
   - Check for remote tracking: `git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null`
   - If it returns a branch name, run `git pull --rebase`; if empty or error, skip the pull
5. If the Sprint field is empty, ask whether to add the issue to the current sprint and do so via MCP if confirmed
6. Add comment: "Starting work on branch `feature/<JIRA_TASK_ID>`."
7. Transition status to "In Progress"

## End of /jira

After completing all steps above, **stop**. Display a summary block:

```
---
Task:   <ISSUE_KEY> — <SUMMARY>
Branch: feature/<ISSUE_KEY>
File:   <jira_folder>/<ISSUE_KEY>.md
Status: In Progress
---
Pronto. Aguardando instruções.
```

Do not begin any implementation work. Do not suggest next steps, generate code, or take any action related to the issue — even if the task is already "In Progress" or has prior context. Wait for the user to give the next instruction explicitly.
