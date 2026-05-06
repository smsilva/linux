---
name: jira
description: Navigate and work on a Jira issue (epic, story, or task) using the jira-workflow skill
---

Use the `jira-workflow` skill for all Jira operations (MCP, task file, comments, transitions, assignments).

$ARGUMENTS — JIRA_ID (epic, story, or task)

**Paths used in this skill:**
- Project config: `.claude/jira/config.md`
- Task file: `.claude/jira/<JIRA_TASK_ID>.md` (e.g. `.claude/jira/PROJ-123.md`)

If `.claude/jira/config.md` exists, read it before any action to get project configuration:
site URL, required fields when creating issues, labels, and owner name.
If it doesn't exist, suggest running `/jira-init` to configure the project.

## Navigation

- If `$ARGUMENTS` is empty:
  - Look for task files matching `.claude/jira/*.md` excluding `config.md`
  - If exactly one is found, read it to get the JIRA_ID and context, and continue from where we left off
  - If multiple are found, list them and ask the user to choose
  - If none are found, ask the user for the JIRA_ID
- Fetch the issue by the received JIRA_ID
- If it's an epic: list associated stories that still need work and ask the user to choose one
- If it's a story:
    - list pending tasks and ask the user to choose one
    - if there are no pending tasks, list all tasks with their status and last comment, and ask the user to choose one
- The final working issue must be a task

## Task file

Stored at `.claude/jira/<JIRA_TASK_ID>.md` (never at the repo root; create `.claude/jira/` if needed).

**Task:** [JIRA_TASK_ID — task title](<JIRA_SITE_URL>/browse/JIRA_TASK_ID)
**Story:** [JIRA_STORY_ID — story title](<JIRA_SITE_URL>/browse/JIRA_STORY_ID)
**Epic:** [JIRA_EPIC_ID — epic title](<JIRA_SITE_URL>/browse/JIRA_EPIC_ID)
**Status:** In Development
**Owner:** <current user name>
**Branch:** feature/JIRA_TASK_ID
**Goal**: What we're trying to accomplish with this task
**Current Progress**: What has been done so far
**What Worked**: Approaches that succeeded and should be repeated or expanded
**What Didn't Work**: Approaches that failed (so they aren't repeated)
**Next Steps**: Clear action items for continuing

## Start task

1. If not assigned, confirm and assign to the current user
2. Create `.claude/jira/<JIRA_TASK_ID>.md` if it doesn't exist (create `.claude/jira/` if needed)
3. If branch `feature/<JIRA_TASK_ID>` **does not exist**:
   - Checkout main and pull latest changes
   - Create branch from main: `git checkout -b feature/<JIRA_TASK_ID>`
4. If branch `feature/<JIRA_TASK_ID>` **already exists** (local or remote):
   - Checkout the branch
   - Run `git pull --rebase` if remote tracking exists
5. If the Sprint field is empty, ask whether to add the issue to the current sprint and do so via MCP if confirmed
6. Add comment: "Starting work on branch `feature/<JIRA_TASK_ID>`."
7. Transition status to "In Progress"
