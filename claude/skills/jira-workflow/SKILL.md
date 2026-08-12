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

The unit of work is a **target status by name** (e.g. "In Development", "In Production"), NOT a single transition. The target is almost never one hop away — reaching it usually means walking several transitions in sequence. Never stop at the first transition and assume you're done.

Loop until the issue's current status equals the target:

1. Use `mcp__atlassian__getTransitionsForJiraIssue` to list transitions available from the **current** status.
2. If a transition leads directly to the target status, take it — you're on the last hop.
3. Otherwise pick the transition that advances **forward** along the workflow toward the target (the next status in the chain), avoiding side-exits like `Blocked`, `Cancel`, `Pause …`, or `Review …` (which move backward). If the repo's `CLAUDE.local.md` documents the chain, use it to choose; otherwise infer the forward step from the status names.
4. Apply it with `mcp__atlassian__transitionJiraIssue` using the `transition.id` (IDs are per-issue — always take them from the fresh `getTransitionsForJiraIssue` output, never reuse an ID from a previous issue or step).
5. Re-fetch transitions and repeat from step 1 until the target status is reached.
6. Update the `Status` field in the task file to the final status.

Two common targets:
- **Start of work** → target "In Development". From a fresh issue this can be several hops (e.g. `New → In Specification → Specified → In Development`), not a single "In Development" transition. Do NOT fall back to a different status (e.g. "In Progress") just because the first hop out of `New` isn't literally named "In Development" — keep walking; the "In Development" status typically appears a few steps in. Only fall back if, after reaching a terminal-forward status, no path to "In Development" exists at all in this workflow.
- **End of work** → target "In Production" (or "Done"/"Closed"). Walk the full chain (e.g. `Developed → In Testing → Tested → Em Homologação → Homologado → In Production`).

**Record the chain the first time it's discovered.** If the repo's `CLAUDE.local.md` does NOT yet document the transition chain for this project/issue-type combination, add a `## Cadeia de transições Jira` (or matching-language heading) section to it once a walk is complete, listing the status names in order with the transition name on each edge:

```
Status A --(Transition name)--> Status B --(Transition name)--> Status C
```

Transition IDs are re-fetched per issue, but the status names and their order are stable for the same project + issue type — that's what makes the recorded chain reusable. An issue may enter the chain partway through (e.g. created already in "In Specification"), so record the whole chain you observe and note the entry point. If the file already documents a chain for this project/issue-type, extend or correct it only when the actually-walked path diverges from what's recorded.

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
