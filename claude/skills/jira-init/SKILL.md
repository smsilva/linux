---
name: jira-init
description: Initialize Jira project config for the current repository, generating .claude/jira/config.md
---

Use the `jira-workflow` skill for MCP operations.

All user-facing messages must use the language specified in the user's CLAUDE.md (e.g. `Always respond in pt-BR`). If no language is specified there, fall back to the system default.

Initializes the Jira configuration for the current project, generating `.claude/jira/config.md`
with required fields discovered via MCP. Should be run once per project.

## Steps

### Step 1 — Reuse config from another project

Ask: "Do you have a `config.md` from another project you want to reuse as a starting point?"

Accept either:
- A **path to a file** (e.g. `~/other-project/.claude/jira/config.md`)
- A **path to a project directory** (look for `.claude/jira/config.md` inside it)

If found, show its contents and ask: "Is this the right project? Reuse as-is or adapt it?"
- **As-is:** copy it to `.claude/jira/config.md` in the current repo and skip to step 9 (.gitignore).
- **Adapt:** use it as a template; project key is already known, jump directly to step 5 (reference issue) to verify/update field values.

If the user declines or provides nothing, continue normally.

### Step 2 — Check existing file

If `.claude/jira/config.md` already exists, show its contents and ask whether to overwrite.

### Step 3 — Fetch site info

In parallel:
- `getAccessibleAtlassianResources` → get `cloudId` and site base URL
- `atlassianUserInfo` → get the logged-in user's display name

### Step 4 — Project selection

Call `getVisibleJiraProjects`. If the response is saved to a file (tool output too large), run:

```bash
python3 ~/.claude/skills/jira-init/scripts/parse_projects.py <path-to-tool-output-file>
```

This prints `KEY | Name | projectTypeKey` per project. Show the list and ask the user to choose.

### Step 5 — Reference issue

Ask: "Do you have an existing Jira issue key from this project to use as a reference for field values? (e.g. `PROJ-123` or full URL like `https://account.atlassian.net/browse/PROJ-123`)"

If provided:
1. Call `getJiraIssueTypeMetaWithFields` for the Story issue type to discover all custom field IDs.
   If the response is saved to a file, run:
   ```bash
   python3 ~/.claude/skills/jira-init/scripts/parse_fields.py <path-to-tool-output-file>
   ```
   The output now includes `schema.type` and `operations`. Collect:
   - All `customfield_XXXXX` IDs that appear here → these are the **writable fields** (they exist on the create screen).
   - For each field, note its `schema_type` and whether `ops` includes `set`.
2. Call `getJiraIssue` with `fields` set to the discovered custom field IDs plus `["labels", "priority", "issuetype", "parent"]`.
3. Extract all non-null/non-empty `customfield_*` values and `labels` → use as **candidate values** for `additional_fields`.
   **Cross-reference rule:** Only include a field in `additional_fields` if it appears in **both**:
   - the create screen metadata (step 5.1) with `ops` containing `set`, AND
   - the reference issue GET response (step 5.2) with a non-null value.
   Fields returned by GET that are **absent from the create screen** are auto-populated by Jira and cannot be sent in creation payloads — do not include them.
4. For fields that pass the cross-reference, determine the correct write format:
   - Fields with `allowedValues`: use `{"id": "<id>"}` from the matching allowed value.
   - Fields with `autoCompleteUrl` but no `allowedValues` (e.g. Team, user pickers): they ARE user-settable — derive the write format from the GET value. For object types, use `{"id": "<id>"}` (drop name/avatar/other metadata). Do NOT treat these as auto-populated just because they have no fixed list.
   - Fields with neither `allowedValues` nor `autoCompleteUrl` and an opaque system schema (e.g. `devsummarycf`, `vulnerabilitycf`, `lexo-rank`): these are system-managed — exclude them.
5. Skip step 6 (field metadata) and step 7 (labels prompt) — values are already known; just confirm with the user.

> **Why discover fields first:** `customfield_*` is not a valid wildcard in the Jira API — only fields explicitly listed in `fields` are returned. Custom fields can have IDs above 11000 (e.g. `customfield_11550`) and are invisible if you hardcode a low range like 10000–10036.

> **Why cross-reference with create screen:** a field present in GET but absent from `getJiraIssueTypeMetaWithFields` is not settable during issue creation — including it causes a 400 error. The authoritative signal is presence in the create screen with `ops: [set]`, not the field's schema type. Fields with `autoCompleteUrl` (e.g. Team) are user-settable even though they have no fixed `allowedValues`.

If not provided, continue to step 6.

### Step 6 — Field metadata discovery (only when no reference issue)

For Story and Task issue types: `getJiraIssueTypeMetaWithFields`.

If the response is saved to a file, run:

```bash
python3 ~/.claude/skills/jira-init/scripts/parse_fields.py <path-to-tool-output-file>
```

This prints `REQUIRED/optional | fieldId | name | allowed values`.

For each non-obvious custom field that has `allowedValues` (and is not `issuetype`, `project`, `reporter`, `summary`):
ask "Should `<name>` (`<fieldId>`) be set on every issue? If so, which value?"

### Step 7 — Confirm labels (only when no reference issue)

Ask: "Are there required labels for the board to filter correctly? (e.g. `Cloud_IDP`)"

### Step 8 — Generate `.claude/jira/config.md`

Create the directory `.claude/jira/` if it doesn't exist, then write `config.md`.
Use the format below. Include the `cloudId` discovered in step 3 and the issue types table from the
project metadata. Add a note about epic linking if detectable from the reference issue or field metadata
(`parent` field accepted → use `parent`; otherwise use `customfield_10014`).

### Step 9 — Storage and `.gitignore`

Ask whether the user wants to version-control Jira files in this repository.

**Yes (version-controlled):**
- Suggest `/jira` as the folder but allow the user to specify another path — use whatever they confirm.
- The chosen path will store task files and will be committed to the repo.

**No (local):**
- Suggest `.claude/jira/` as the Jira folder but allow the user to specify another path — use whatever they confirm.
- Then check `.gitignore`:
  1. If `.claude/` or `.claude/**` is already listed → skip.
  2. If `.claude/jira/` is already listed → skip.
  3. Otherwise: suggest adding `.claude/` to `.gitignore` and ask before making any change.

**After the decision:** record the resolved Jira folder path in `config.md` under `## Paths` (see format below). `config.md` itself always lives at `.claude/jira/config.md` regardless of where task files are stored.

---

## Format of `.claude/jira/config.md`

```markdown
# Jira Project Config

**Project:** <PROJECT_KEY>
**Site:** <https://account.atlassian.net>
**cloudId:** <uuid>
**Owner:** <user display name>

## Paths

- **Jira folder:** `/jira` *(or `.claude/jira/` if local — always the folder containing task files)*
- **Config:** `.claude/jira/config.md` *(always here, regardless of Jira folder)*

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
