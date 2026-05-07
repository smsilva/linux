---
name: jira-workflow
description: Primitives for interacting with Jira via MCP Atlassian — configure MCP, create/update task files, comment, transition status, and assign issues.
---

# jira-workflow

**Paths convention:**
- Project config: `.claude/jira/config.md` (always here)
- Task file: `<jira_folder>/<JIRA_TASK_ID>.md` — read `## Paths` → Jira folder from `config.md`; default `.claude/jira/`

## Task file format (authoritative — do not deviate)

Every task file must be written using **exactly** this structure. Replace each `{{PLACEHOLDER}}` with the actual value; omit optional lines when the value is empty.

```markdown
# {{ISSUE_KEY}}: {{SUMMARY}}

**Task:** [{{ISSUE_KEY}} — {{SUMMARY}}]({{SITE}}/browse/{{ISSUE_KEY}})
**Story:** [{{STORY_KEY}} — {{STORY_SUMMARY}}]({{SITE}}/browse/{{STORY_KEY}})
**Epic:** [{{EPIC_KEY}} — {{EPIC_SUMMARY}}]({{SITE}}/browse/{{EPIC_KEY}})
**Status:** {{STATUS}}
**Owner:** {{ASSIGNEE}}
**Branch:** feature/{{ISSUE_KEY}}
**Sprint:** {{SPRINT}}

## Description

{{DESCRIPTION}}

## Work log

### Goal

What we're trying to accomplish with this task

### Current Progress

What has been done so far

### What Worked

Approaches that succeeded and should be repeated or expanded

### What Didn't Work

Approaches that failed (so they aren't repeated)

### Next Steps

Clear action items for continuing
```

Rules:
- The task file is a **structured document, not a user-facing response** — language settings (e.g. `Always respond in pt`) do NOT apply to it. All field names and section headers must be exactly as shown above, in English.
- Title separator is `:` (not `—`)
- `**Owner:**` — not `**Assignee:**`, `**Responsável:**`, or any other label
- `## Description` — not `## Objetivo`, `## Descrição`, `## Descripción`, or any translation
- `## Work log` with all five `###` subsections — always include, even if empty
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
1. Read `.claude/jira/config.md` → `## Paths` → **Jira folder** value.
2. If absent or `config.md` doesn't exist, default to `.claude/jira/`.

Task file path: `<jira_folder>/<JIRA_TASK_ID>.md` (create the folder if needed).

If the resolved Jira folder is `.claude/jira/`: run `grep -xF '.claude/' .gitignore` and `grep -xF '.claude/**' .gitignore` — if neither matches exactly, suggest adding `.claude/` to `.gitignore` and ask before making any change.

**Do NOT use the Write tool to create the task file.** Use the script below — it copies the template and substitutes placeholders, ensuring the format is always correct regardless of the issue description's internal structure.

Steps:
1. Write the issue description verbatim to `/tmp/jira_description.txt` using the Write tool.
2. Run the creation script, substituting each `<VALUE>` with actual data from the issue:

```bash
python3 ~/.claude/skills/jira-workflow/create-task-file.py \
  --template ~/.claude/skills/jira-workflow/task-template.md \
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
  --description-file /tmp/jira_description.txt
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

If `.claude/jira/config.md` exists in the current project, apply the `additional_fields` defined in its "Issue creation — required fields" section before creating any issue.

After creation, link to the epic via `mcp__atlassian__editJiraIssue` with `customfield_10014: "<EPIC_KEY>"` if the `parent` field is not accepted by the project's issue type.
