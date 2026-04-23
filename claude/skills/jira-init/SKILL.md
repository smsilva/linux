---
name: jira-init
description: Initialize Jira project config for the current repository, generating .claude/JIRA-PROJECT.md
---

Use the `jira-workflow` skill for MCP operations.

Initializes the Jira configuration for the current project, generating `.claude/JIRA-PROJECT.md` with
required fields discovered via MCP. Should be run once per project.

## Steps

1. If `.claude/JIRA-PROJECT.md` already exists, show its contents and ask whether to overwrite.

2. Via MCP, in parallel:
   - `getAccessibleAtlassianResources` → get `cloudId` and site base URL
   - `atlassianUserInfo` → get the logged-in user's display name

3. `getVisibleJiraProjects` → list available projects and ask the user to choose one.

4. For the chosen project:
   - `getJiraProjectIssueTypesMetadata` → list issue types
   - For Story and Task types: `getJiraIssueTypeMetaWithFields` → list `required` fields
     and fields with `allowedValues` (custom fields potentially required by the board)

5. Ask the user:
   - "Are there required labels for the board to filter correctly?" (e.g. `Cloud_IDP`)
   - For each non-obvious custom field discovered: "Is the `<name>` field required? If so, what value should be used?"

6. Generate `.claude/JIRA-PROJECT.md` using the format below.

7. Ask: "Should this file be committed (team config) or added to `.gitignore` (local config)?"
   - If local: add `JIRA-PROJECT.md` to `.gitignore`

## Format of `.claude/JIRA-PROJECT.md`

```markdown
# Jira Project Config

**Project:** <PROJECT_KEY>
**Site:** <https://account.atlassian.net>
**Owner:** <user display name>

## Issue creation — required fields

When creating any issue via `mcp__atlassian__createJiraIssue`, include in `additional_fields`:

```json
{
  "labels": ["<LABEL>"],
  "<customfield_xxxxx>": <value>
}
```

> `<customfield_xxxxx>` — <field name>: <why it's required, e.g. "board filters by this field">

## Board notes

<notes about filters, sprints, epics, special fields>
```
