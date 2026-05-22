---
name: jira-workflow
description: Primitives for interacting with Jira via MCP Atlassian — configure MCP, create/update task files, comment, transition status, and assign issues.
user-invocable: false
---

# jira-workflow

**Paths convention:**
- Project config: `.jira/config.md` (always here)
- Task file: `<jira_folder>/<JIRA_TASK_ID>.md` — read `## Paths` → Jira folder from `config.md`; default `.jira/`

## Task file

This file will be created and updated by the skill to keep track of the issue's status, owner, branch, and work log. It serves as the authoritative source of truth for the issue's current state and history of actions taken.

Stored at `<jira_folder>/<JIRA_TASK_ID>.md` — resolve `<jira_folder>` from `config.md` → `## Paths`; default `.jira/`. 

## Task file format

Should use the template at `jira-workflow/templates/task.md`.

Rules:
- The task file is a **structured document, not a user-facing response** — language settings (e.g. `Always respond in pt`) do NOT apply to it.
- No extra fields (no `**Repo:**`, no YAML frontmatter, no `**Epic URL:**`)
- Paste the Jira description verbatim under `## Description` — do not summarize or rewrite it

## 1. Get accessible resources and current user

Use `mcp__atlassian__getAccessibleAtlassianResources` to get the `cloudId` of the Atlassian site.

Use `mcp__atlassian__atlassianUserInfo` to get the `accountId` of the logged-in user.

## 2. Fetch the issue

Use `mcp__atlassian__getJiraIssue` with `responseContentFormat: "markdown"`.

Fields needed for the task file: `key`, `summary`, `status`, `description`, `assignee`, `sprint`, `epic`.

## 3. Create or update task file

Resolve the Jira folder path before writing any file:
1. Read `.jira/config.md` → `## Paths` → **Jira folder** value.
2. If absent or `config.md` doesn't exist, default to `.jira/`.

Task file path: `<jira_folder>/<JIRA_TASK_ID>.md` (create the folder if needed).

If the resolved Jira folder is `.jira/`: run `grep -xF '.jira/' .gitignore` — if it doesn't match exactly, suggest adding `.jira/` to `.gitignore` and ask before making any change.

**Do NOT use the Write tool to create the task file.** Use the script below — it copies the template and substitutes placeholders, ensuring the format is always correct regardless of the issue description's internal structure.

Steps:
1. Write the issue description verbatim to `/tmp/jira_description_<JIRA_TASK_ID>.txt` using the Write tool.
2. Run the creation script, substituting each `<VALUE>` with actual data from the issue:

```bash
skill_dir="$(readlink -f ~/.claude/skills/jira-workflow)"
python3 "${skill_dir}/scripts/create-task-file.py" \
  --output <jira_folder>/<ISSUE_KEY>.md \
  --issue-key <ISSUE_KEY> \
  --summary "<SUMMARY>" \
  --site "<SITE>" \
  --story-key "<STORY_KEY>" \
  --story-summary "<STORY_SUMMARY>" \
  --epic-key "<EPIC_KEY>" \
  --epic-summary "<EPIC_SUMMARY>" \
  --status "<STATUS>" \
  --assignee "<ASSIGNEE>" \
  --sprint "<SPRINT>" \
  --description-file /tmp/jira_description_<JIRA_TASK_ID>.txt
```

Omit `--story-key`/`--story-summary`, `--epic-key`/`--epic-summary`, or `--sprint` entirely if the values are empty — the script removes those lines automatically.

Sync task file content as a comment on the issue (via `mcp__atlassian__addCommentToJiraIssue` with `contentFormat: "markdown"`) at these moments:
- When creating the task file for the first time
- When transitioning the issue status
- When closing out the work (handoff or completion)

## 4. Transition status

1. Use `mcp__atlassian__getTransitionsForJiraIssue` to list available transitions.
2. Identify the target transition ID by name (e.g. "In Progress").
3. Use `mcp__atlassian__transitionJiraIssue` with the `transition.id` found.
4. Update the `Status` field in the task file.

## 5. Assign issue to current user

Use `mcp__atlassian__editJiraIssue` with:

```json
{
  "fields": {
    "assignee": { "accountId": "<current_user_account_id>" }
  }
}
```

## 6. Create issues (stories or tasks)

Use `mcp__atlassian__createJiraIssue` with `issueTypeName`, `summary`, and `projectKey`.

If `.jira/config.md` exists in the current project, apply the `additional_fields` defined in its "Issue creation — required fields" section before creating any issue.

After creation, link to the epic via `mcp__atlassian__editJiraIssue` with `customfield_10014: "<EPIC_KEY>"` if the `parent` field is not accepted by the project's issue type.
