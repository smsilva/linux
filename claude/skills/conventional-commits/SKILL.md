---
name: conventional-commits
description: Create commit messages following the Conventional Commits specification (https://www.conventionalcommits.org/en/v1.0.0/).
license: MIT
---

# conventional-commits skill

Create commit messages following the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

## Format

```
<type>(<scope>): <description>
```

- **type**: what kind of change
- **scope**: what was changed (file, module, ticket ID) — optional but preferred
- **description**: imperative, lowercase, no period at the end

## Types

| Type       | When to use |
|------------|-------------|
| `feat`     | New feature or behavior added |
| `fix`      | Bug fix |
| `refactor` | Code change that is neither a fix nor a feature |
| `chore`    | Maintenance, tooling, dependencies, releases |
| `docs`     | Documentation only |
| `test`     | Adding or updating tests |
| `ci`       | CI/CD pipeline changes |
| `perf`     | Performance improvement |
| `revert`   | Reverts a previous commit |

## Scope

Use the most specific relevant identifier:

- **File or path**: `scripts/bin/arm`, `scripts/bash_config`
- **Module or feature**: `auth`, `content-hub`, `appearance`
- **Ticket ID**: `JIRA-44390`, `PROJ-123`
- **Branch name** when releasing: `main`

## Examples

```
feat(scripts/bin/foo): add --dry-run option
fix(JIRA-41303): avoid 431 error in authorization integration
refactor(scripts/bin/drm): use docker list --format option
chore(main): release 3.74.0
docs(README.md): add utilities section
feat(JIRA-32740): add search for solutions
```

## Rules

- Description in imperative mood: "add", "fix", "remove" — not "added", "fixes", "removed"
- No capital letter at the start of the description
- No period at the end
- Keep the subject line under 72 characters
- Breaking changes: append `!` after the type/scope — `feat(api)!: remove endpoint`

## When writing the commit

1. Look at `git diff --staged` to understand what changed
2. Pick the `type` that best describes the nature of the change
3. Set the `scope` to the most specific relevant path or identifier
4. Write the description summarising **what** changed, not **how**
