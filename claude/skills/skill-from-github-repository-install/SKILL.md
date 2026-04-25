---
name: skill-from-github-repository-install
description: Use when the user invokes /skill-from-github-repository-install with a GitHub URL pointing to a skill directory. Installs the skill by cloning the repository and creating a symlink into the Claude skills directory.
---

# skill-from-github-repository-install

Install a Claude skill from a GitHub repository URL by cloning the repo and symlinking the skill.

## Input

The user provides a GitHub URL pointing to a skill directory:
```
https://github.com/{owner}/{repo}/tree/{branch}/{path/to/skill-name}
```

Example: `https://github.com/getsentry/skills/tree/main/skills/security-review`

## Steps

### 1. Parse the URL

Extract from the URL:
- `owner` — e.g. `getsentry`
- `repo` — e.g. `skills`
- `branch` — e.g. `main`
- `skill_path` — path inside the repo, e.g. `skills/security-review`
- `skill_name` — last segment of `skill_path`, e.g. `security-review`
- `clone_url` — `https://github.com/{owner}/{repo}.git`
- `local_repo` — `${HOME}/.git/{owner}/{repo}`
- `skill_source` — `${local_repo}/{skill_path}`

### 2. Check if skill is already installed

Run both checks:
```bash
ls "${PWD}/.claude/skills/${skill_name}" 2>/dev/null && echo local || echo not-local
ls "${HOME}/.claude/skills/${skill_name}" 2>/dev/null && echo global || echo not-global
```

If found, check whether it is a symlink:

**If it is a symlink** — the skill came from a git repo managed by this tool. Invoke the `skill-from-github-repository-update` skill to pull the latest version and **stop** (do not reinstall):
```bash
if [ -L "${HOME}/.claude/skills/${skill_name}" ] || [ -L "${PWD}/.claude/skills/${skill_name}" ]; then
  # delegate to skill-from-github-repository-update
fi
```

**If it is a regular directory** (not a symlink) — show where it is installed and ask the user:

```
A skill "${skill_name}" já está instalada em <path> (não é um symlink).
Deseja substituir a skill existente? (s/n)
```

- If **n**: abort.
- If **s**: remove the existing entry before proceeding:
  ```bash
  rm -rf "${HOME}/.claude/skills/${skill_name}"
  # or for local:
  rm -rf "${PWD}/.claude/skills/${skill_name}"
  ```

### 3. Clone or update the repository

```bash
mkdir -p "${HOME}/.git/${owner}"
```

If `${local_repo}` already exists, pull instead of clone:
```bash
if [ -d "${local_repo}/.git" ]; then
  git -C "${local_repo}" pull --ff-only
else
  git -C "${HOME}/.git/${owner}" clone "${clone_url}" --depth 1 --branch "${branch}"
fi
```

### 4. Choose install scope

Check whether the project has a local skills directory:
```bash
ls "${PWD}/.claude/skills" 2>/dev/null && echo true || echo false
```

If **true**, ask the user:

```
Você já possui skills instaladas na pasta de skills do projeto.

Deseja instalar a skill localmente (dentro da pasta do projeto) ou globalmente (na pasta de skills do claude)?

1=local
2=global
```

- **1 (local)**: `target="${PWD}/.claude/skills/${skill_name}"`
- **2 (global)**: `target="${HOME}/.claude/skills/${skill_name}"`

If **false** (no local skills dir), install globally without asking:
```bash
target="${HOME}/.claude/skills/${skill_name}"
```

### 5. Create the symlink

```bash
ln -s "${skill_source}" "${target}"
```

### 6. Confirm

Report the result:
```
Skill "${skill_name}" instalada com sucesso.
Origem:  ${skill_source}
Destino: ${target}
```

## Error cases

| Situation | Action |
|-----------|--------|
| URL format not recognized | Ask user to provide a full GitHub tree URL |
| `skill_source` does not exist after clone | Warn: path not found in repo; show what exists under `${local_repo}` |
| `ln` fails (permissions) | Show the exact error and suggest running manually |
| Git clone fails | Show git output; suggest checking URL or network |
