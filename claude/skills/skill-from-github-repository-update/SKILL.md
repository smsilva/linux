---
name: skill-from-github-repository-update
description: Use when the user invokes /skill-from-github-repository-update to update one or more symlink-based skills by pulling their source git repositories.
---

# skill-from-github-repository-update

Update installed skills that were installed as symlinks by pulling their underlying git repositories.

## Input

Optional skill name argument:
```
/skill-from-github-repository-update [skill-name]
```

- **Without argument** — list all updatable (symlink) skills and ask which to update.
- **With argument** — update that skill directly.

## Steps

### 1. Discover updatable skills

Use the `list-symlink-skills` script (in `scripts/` next to this file):
```bash
"${SKILL_DIR}/scripts/list-symlink-skills"
```

Where `SKILL_DIR` is the base directory of this skill (provided at skill load time).

### 2. If no argument was given — show list and ask

If no updatable skills found: abort.
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

### 3. Update the skill(s)

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

### 4. Confirm

`update-skill` prints for each skill:
```
✓ skill-name  →  /home/user/.git/owner/repo
```

## Error cases

| Situation | Action |
|-----------|--------|
| Named skill not found as symlink | Abort with message |
| Named skill exists but not a symlink | Abort, suggest manual update |
| `.git` repo not found at expected path | Abort showing the resolved path |
| `git pull` fails (conflict, network) | Show full git output |
