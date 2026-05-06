---
name: jira-workflow
description: Primitives for interacting with Jira via MCP Atlassian — configure MCP, create/update task files, comment, transition status, and assign issues.
---

# jira-workflow

**Paths convention:**
- Project config: `.claude/jira/config.md` (always here)
- Task file: `<jira_folder>/<JIRA_TASK_ID>.md` — read `## Paths` → Jira folder from `config.md`; default `.claude/jira/`

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

If the resolved Jira folder is `.claude/jira/` and `.claude/` is not in `.gitignore`, suggest adding it and ask before making any change.

```markdown
# <ISSUE_KEY>: <summary>

**Status:** <status>
**Link:** <Jira issue URL>
**Assignee:** <assignee name>
**Sprint:** <current sprint> *(optional)*
**Epic:** <epic> *(optional)*

## Description

<description>
```

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
