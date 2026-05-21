---
name: skill-from-github-repository-update
description: Use when the user invokes /skill-from-github-repository-update to update one or more symlink-based skills by pulling their source git repositories.
disable-model-invocation: true
---

# skill-from-github-repository-update

Update installed skills that were installed as symlinks by pulling their underlying git repositories.

## Input

Optional skill name or special argument:
```
/skill-from-github-repository-update [skill-name|bootstrap|repair]
```

- **Without argument** — list all updatable (symlink) skills and ask which to update; broken symlinks are detected and repaired automatically first.
- **With skill name** — update that skill directly.
- **`bootstrap`** — sync registry from symlinks, reinstall missing skills, and repair broken symlinks.
- **`repair`** — detect and repair all broken symlinks using URLs from the registry.

## Steps

### 1. Discover skills

Run both discovery scripts:
```bash
"${SKILL_DIR}/scripts/list-symlink-skills"
"${SKILL_DIR}/scripts/list-broken-skills"
```

`list-symlink-skills` returns valid symlinks (updatable).
`list-broken-skills` returns symlinks whose target path is missing (repairable).

Where `SKILL_DIR` is the base directory of this skill (provided at skill load time).

### 2. If argument is `bootstrap` — sync registry, reinstall missing, and repair broken

#### 2a. Discover installed symlink skills

Run the `sync-registry` script:
```bash
"${SKILL_DIR}/scripts/sync-registry"
```

This outputs lines of the form `skill_name github_url`, one per discovered symlink whose target matches `~/.git/{owner}/{repo}/...`.

#### 2b. Sync `third-party.md`

Registry path: `${HOME}/.claude/skills/third-party.md`

For each discovered entry:
- If the skill is **not in the registry**: insert a new row in alphabetical order.
- If the skill is **already in the registry with a different URL**: update the URL.
- If the skill is **already in the registry with the same URL**: skip.

If the registry file does not exist, create it with the standard header before inserting:
```markdown
# Third-party skills

Skills installed from external GitHub repositories via `/skill-from-github-repository-install`.
Run `/skill-from-github-repository-update bootstrap` to reinstall all entries on a new machine.

| skill | url |
|-------|-----|
```

Report a summary of what was added or updated.

#### 2c. Reinstall missing skills

Read every row in `third-party.md`. For each `skill_name`:
```bash
global_link="${HOME}/.claude/skills/${skill_name}"
local_link="${PWD}/.claude/skills/${skill_name}"
```

If **neither** exists as a symlink, install it by following the full install flow from `skill-from-github-repository-install` (parse URL → clone/pull repo → create symlink). Do **not** re-register in `third-party.md` (already present).

If it already exists (symlink or directory), skip it.

Report each action:
```
✓ diagnose  — already installed
✓ pptx      — reinstalled from https://github.com/anthropics/skills/tree/main/skills/pptx
```

#### 2d. Repair broken symlinks

```bash
"${SKILL_DIR}/scripts/list-broken-skills" | while read -r skill; do
  "${SKILL_DIR}/scripts/repair-skill" "${skill}"
done
```

Report each result.

### 2b. If argument is `repair` — repair broken symlinks

Run `list-broken-skills`. If none found:
```
Nenhuma skill com symlink quebrado encontrada.
```

Otherwise, repair each:
```bash
"${SKILL_DIR}/scripts/list-broken-skills" | while read -r skill; do
  "${SKILL_DIR}/scripts/repair-skill" "${skill}"
done
```

### 3. If no argument was given — repair broken first, then show list

#### 3a. Repair broken symlinks (automatic)

Run `list-broken-skills`. If any are found, report and repair them automatically before proceeding:
```bash
"${SKILL_DIR}/scripts/list-broken-skills" | while read -r skill; do
  "${SKILL_DIR}/scripts/repair-skill" "${skill}"
done
```

#### 3b. Show updatable skills and ask

If no valid symlinks found: abort.
```
Nenhuma skill instalada via symlink encontrada.
```

Otherwise, display the list in alphabetical order and ask the user which to update:
```
Skills disponíveis para atualização:

  1. bash-scripts
  2. security-review
  3. skill-from-github-repository-install
  ...

Digite o número ou nome da skill (ou "all" para atualizar todas):
```

### 4. Update the skill(s)

Use the `update-skill` script for each selected skill:
```bash
"${SKILL_DIR}/scripts/update-skill" "${skill_name}"
```

For `all`, pipe the list into the script:
```bash
"${SKILL_DIR}/scripts/list-symlink-skills" | while read -r skill; do
  "${SKILL_DIR}/scripts/update-skill" "${skill}"
done
```

`update-skill` handles: resolving install path → symlink target → git repo root → `git pull --ff-only`.
When multiple skills share the same repo, each `update-skill` call is independent; git will report "Already up to date" for subsequent calls to the same repo.

### 5. Confirm

`update-skill` prints for each skill:
```
✓ skill-name  →  /home/user/.git/owner/repo
```

`repair-skill` prints for each skill:
```
✓ skill-name  →  /home/user/.git/owner/repo (clonado)
  symlink OK: /home/user/.git/owner/repo/skills/skill-name
```

## Error cases

| Situation | Action |
|-----------|--------|
| Named skill not found as symlink | Abort with message |
| Named skill exists but not a symlink | Abort, suggest manual update |
| `.git` repo not found at expected path | Abort showing the resolved path |
| `git pull` fails (conflict, network) | Show full git output |
| Broken skill not found in registry | Abort: skill must be registered in `third-party.md` to be repaired |
| Registry URL cannot be parsed | Abort showing the URL that failed to parse |
| Symlink still broken after clone | Abort showing the symlink target path |
