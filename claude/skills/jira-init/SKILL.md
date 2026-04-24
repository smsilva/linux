---
name: jira-init
description: Initialize Jira project config for the current repository, generating .claude/JIRA-PROJECT.md
---

Use the `jira-workflow` skill for MCP operations.

Initializes the Jira configuration for the current project, generating `.claude/JIRA-PROJECT.md` with
required fields discovered via MCP. Should be run once per project.

## Steps

### Step 0 — Reuse config from another project

Ask: "Do you have a `JIRA-PROJECT.md` from another project you want to reuse as a starting point?"

Accept either:
- A **path to a file** (e.g. `~/other-project/.claude/JIRA-PROJECT.md`)
- A **path to a project directory** (look for `.claude/JIRA-PROJECT.md` inside it)

If found, show its contents and ask: "Is this the right project? Reuse as-is or adapt it?"
- **As-is:** copy it to `.claude/JIRA-PROJECT.md` in the current repo and skip to step 8 (.gitignore).
- **Adapt:** use it as a template; project key is already known, jump directly to step 4 (reference issue) to verify/update field values.

If the user declines or provides nothing, continue normally.

### Step 1 — Check existing file

If `.claude/JIRA-PROJECT.md` already exists, show its contents and ask whether to overwrite.

### Step 2 — Fetch site info

In parallel:
- `getAccessibleAtlassianResources` → get `cloudId` and site base URL
- `atlassianUserInfo` → get the logged-in user's display name

### Step 3 — Project selection

Call `getVisibleJiraProjects`. If the response is saved to a file (tool output too large), run:

```bash
python3 ~/.claude/skills/jira-init/scripts/parse_projects.py <path-to-tool-output-file>
```

This prints `KEY | Name | projectTypeKey` per project. Show the list and ask the user to choose.

### Step 4 — Reference issue

Ask: "Do you have an existing Jira issue key from this project to use as a reference for field values? (e.g. `PROJ-123` or full URL like `https://account.atlassian.net/browse/PROJ-123`)"

If provided:
- Call `getJiraIssue` with `fields: ["labels", "customfield_*", "priority", "issuetype", "parent"]`
- Extract all set `customfield_*` values and `labels` → use as **ground truth** for `additional_fields`
- Skip step 5 (field metadata) and step 6 (labels prompt) — values are already known; just confirm with the user

If not provided, continue to step 5.

### Step 5 — Field metadata discovery (only when no reference issue)

For Story and Task issue types: `getJiraIssueTypeMetaWithFields`.

If the response is saved to a file, run:

```bash
python3 ~/.claude/skills/jira-init/scripts/parse_fields.py <path-to-tool-output-file>
```

This prints `REQUIRED/optional | fieldId | name | allowed values`.

For each non-obvious custom field that has `allowedValues` (and is not `issuetype`, `project`, `reporter`, `summary`):
ask "Should `<name>` (`<fieldId>`) be set on every issue? If so, which value?"

### Step 6 — Confirm labels (only when no reference issue)

Ask: "Are there required labels for the board to filter correctly? (e.g. `Cloud_IDP`)"

### Step 7 — Generate `.claude/JIRA-PROJECT.md`

Use the format below. Include the `cloudId` discovered in step 2 and the issue types table from the
project metadata. Add a note about epic linking if detectable from the reference issue or field metadata
(`parent` field accepted → use `parent`; otherwise use `customfield_10014`).

### Step 8 — `.gitignore` handling

Before touching `.gitignore`:
1. Check if `.claude/` or `.claude/**` is already listed → if yes, skip entirely (file is already excluded).
2. Check if `JIRA-PROJECT.md` is already listed → if yes, skip.
3. Otherwise ask: "Commit this file (team config) or keep it local (add to `.gitignore`)?"
   - If local: add `.claude/JIRA-PROJECT.md` to `.gitignore`.

---

## Format of `.claude/JIRA-PROJECT.md`

```markdown
# Jira Project Config

**Project:** <PROJECT_KEY>
**Site:** <https://account.atlassian.net>
**cloudId:** <uuid>
**Owner:** <user display name>

## Issue creation — required fields

When creating any issue via `mcp__atlassian__createJiraIssue`, include in `additional_fields`:

```json
{
  "labels": ["<LABEL>"],
  "<customfield_xxxxx>": <value>
}
```

> `<customfield_xxxxx>` — <field name>: <why it's set, e.g. "board filters by this field">

Use `contentFormat: "markdown"` for description and comment fields.

## Issue types

| Name | ID | Hierarchy |
|------|----|-----------|
| Epic | ... | 1 |
| Story | ... | 0 |
| Task | ... | 0 |

## Board notes

- Epic linking: use `parent` field (or `customfield_10014` if `parent` is not accepted)
- Sprint: `customfield_10020`
- Story Points: `customfield_10034`
- <any other project-specific notes>

> Re-run `/jira-init` to update this file if project structure changes.
```
