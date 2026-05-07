---
name: jira-workflow
description: Primitives for interacting with Jira via MCP Atlassian — configure MCP, create/update task files, comment, transition status, and assign issues.
---

# jira-workflow

**Paths convention:**
- Project config: `.claude/jira/config.md` (always here)
- Task file: `<jira_folder>/<JIRA_TASK_ID>.md` — read `## Paths` → Jira folder from `config.md`; default `.claude/jira/`

## 0. Read task template (always first)

Use the Read tool to read `~/.claude/skills/jira-workflow/task-template.md` **before doing anything else in this skill**. Keep the content in context — it is the required format for every task file. Never write a task file without having read this template in the current session.

## 1. Get accessible resources and current user

Use `mcp__atlassian__getAccessibleAtlassianResources` to get the `cloudId` of the Atlassian site.

Use `mcp__atlassian__atlassianUserInfo` to get the `accountId` of the logged-in user.

## 2. Fetch the issue

Use `mcp__atlassian__getJiraIssue` with `responseContentFormat: "markdown"`.

Fields needed for the task file: `key`, `summary`, `status`, `description`, `assignee`, `sprint`, `epic`.

## 3. Create or update task file

Resolve the Jira folder path before writing any file:
1. Read `.claude/jira/config.md` → `## Paths` → **Jira folder** value.
2. If absent or `config.md` doesn't exist, default to `.claude/jira/`.

Task file path: `<jira_folder>/<JIRA_TASK_ID>.md` (create the folder if needed).

If the resolved Jira folder is `.claude/jira/`: run `grep -xF '.claude/' .gitignore` and `grep -xF '.claude/**' .gitignore` — if neither matches exactly, suggest adding `.claude/` to `.gitignore` and ask before making any change.

To create the task file:
1. **Use the Read tool** to read `~/.claude/skills/jira-workflow/task-template.md` — do not write the task file without reading this first.
2. Substitute every `{{PLACEHOLDER}}` with the actual value from the issue:
   - `{{ISSUE_KEY}}` → issue key (e.g. `PLTF-3`)
   - `{{SUMMARY}}` → issue summary
   - `{{SITE}}` → site URL from `config.md` (e.g. `https://smsilva.atlassian.net`)
   - `{{STORY_KEY}}` → parent story key (omit the `**Story:**` line if none)
   - `{{STORY_SUMMARY}}` → parent story summary
   - `{{EPIC_KEY}}` → epic key (omit the `**Epic:**` line if none)
   - `{{EPIC_SUMMARY}}` → epic summary
   - `{{STATUS}}` → current issue status
   - `{{ASSIGNEE}}` → assignee display name
   - `{{SPRINT}}` → current sprint name, or remove the line if empty
   - `{{DESCRIPTION}}` → issue description in markdown
3. Write the result to `<jira_folder>/<JIRA_TASK_ID>.md`

Do not rename fields, reorder sections, or add fields not in the template.

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

If `.claude/jira/config.md` exists in the current project, apply the `additional_fields` defined in its "Issue creation — required fields" section before creating any issue.

After creation, link to the epic via `mcp__atlassian__editJiraIssue` with `customfield_10014: "<EPIC_KEY>"` if the `parent` field is not accepted by the project's issue type.
