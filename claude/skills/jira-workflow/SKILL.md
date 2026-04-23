---
name: jira-workflow
description: Primitives for interacting with Jira via MCP Atlassian — configure MCP, create/update JIRA.md, comment, transition status, and assign issues.
---

# jira-workflow

## 1. Check and configure the Atlassian MCP

If the Atlassian MCP server is not active, run:

```
claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/mcp
```

Add read-only permissions to `.claude/settings.local.json` so Claude doesn't prompt for every lookup:

```json
{
  "permissions": {
    "allow": [
      "mcp__atlassian__atlassianUserInfo",
      "mcp__atlassian__getJiraIssue",
      "mcp__atlassian__getAccessibleAtlassianResources",
      "mcp__atlassian__searchJiraIssuesUsingJql",
      "mcp__atlassian__search",
      "mcp__atlassian__getTransitionsForJiraIssue",
      "mcp__atlassian__getConfluencePage",
      "mcp__atlassian__getConfluenceSpaces",
      "mcp__atlassian__getPagesInConfluenceSpace",
      "mcp__atlassian__getConfluencePageDescendants",
      "mcp__atlassian__getConfluencePageFooterComments",
      "mcp__atlassian__getConfluencePageInlineComments",
      "mcp__atlassian__getConfluenceCommentChildren",
      "mcp__atlassian__getVisibleJiraProjects",
      "mcp__atlassian__getJiraProjectIssueTypesMetadata",
      "mcp__atlassian__getJiraIssueTypeMetaWithFields",
      "mcp__atlassian__getIssueLinkTypes",
      "mcp__atlassian__getJiraIssueRemoteIssueLinks",
      "mcp__atlassian__lookupJiraAccountId",
      "mcp__atlassian__fetch",
      "mcp__atlassian__searchConfluenceUsingCql"
    ]
  }
}
```

## 2. Get accessible resources and current user

Use `mcp__atlassian__getAccessibleAtlassianResources` to get the `cloudId` of the Atlassian site.

Use `mcp__atlassian__atlassianUserInfo` to get the `accountId` of the logged-in user.

## 3. Fetch the issue

Use `mcp__atlassian__getJiraIssue` with `responseContentFormat: "markdown"`.

Fields needed for JIRA.md: `key`, `summary`, `status`, `description`, `assignee`, `sprint`, `epic`.

## 4. Create or update JIRA.md

`JIRA.md` lives at the repo root **on the working branch only**.

Verify `JIRA.md` is in `.gitignore`; add it if missing.

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

Sync JIRA.md content as a comment on the issue (via `mcp__atlassian__addCommentToJiraIssue` with `contentFormat: "markdown"`) at these moments:
- When creating JIRA.md for the first time
- When transitioning the issue status
- When closing out the work (handoff or completion)

## 5. Transition status

1. Use `mcp__atlassian__getTransitionsForJiraIssue` to list available transitions.
2. Identify the target transition ID by name (e.g. "In Progress").
3. Use `mcp__atlassian__transitionJiraIssue` with the `transition.id` found.
4. Update the `Status` field in JIRA.md.

## 6. Assign issue to current user

Use `mcp__atlassian__editJiraIssue` with:

```json
{
  "fields": {
    "assignee": { "accountId": "<current_user_account_id>" }
  }
}
```

## 7. Create issues (stories or tasks)

Use `mcp__atlassian__createJiraIssue` with `issueTypeName`, `summary`, and `projectKey`.

If `.claude/JIRA-PROJECT.md` exists in the current project, apply the `additional_fields` defined in its "Issue creation — required fields" section before creating any issue.

After creation, link to the epic via `mcp__atlassian__editJiraIssue` with `customfield_10014: "<EPIC_KEY>"` if the `parent` field is not accepted by the project's issue type.
