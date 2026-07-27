# Handoff por-branch, dual-mode, integrado ao Jira — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Substituir o `HANDOFF.md` único na raiz por handoff pertencente à branch corrente, com dois modos (Jira e local) e sync opt-in para o Jira.

**Architecture:** São arquivos de skill (Markdown de instruções para o agente), não código. Cada tarefa edita um `SKILL.md`, o template do task file ou um arquivo de regra. "Testar" = ler/grep o resultado e conferir que as instruções cobrem o comportamento decidido na spec. Sem código, sem suíte de testes, sem commits automáticos.

**Tech Stack:** Markdown; skills do Claude Code; convenção de paths do `jira-workflow`.

## Global Constraints

- Skills escritos em inglês (regra `language.md`); termos técnicos não traduzidos.
- Não repetir nome da pasta pai em nome de arquivo aninhado.
- Detecção de modo: existe `.jira/config.md` **e** task file para a branch corrente → modo Jira; senão → modo local.
- Modo Jira: branch é `feature/<JIRA_ID>`; task file em `<jira_folder>/<JIRA_ID>.md` (resolver `<jira_folder>` de `.jira/config.md` → `## Paths`; default `.jira/`).
- Modo local: handoff em `.handoff/<branch>.md`.
- Marcador do comentário Jira e da seção: cabeçalho fixo `## Handoff` (sem ícone).
- `--share` publica **novo comentário a cada vez**; retomada usa sempre o comentário `## Handoff` **mais recente**. Sem upsert.
- `.handoff/` no `.gitignore` é **opt-in**: `grep -xF '.handoff/' .gitignore`; se não casar, sugerir e perguntar antes de mexer.
- Subseções do handoff (verbatim): `Why`, `In Progress`, `Open Questions / Hypotheses`, `Known Broken`, `How to Resume`, `Next Steps`.
- Linha-rodapé verbatim: `Before trusting anything time-sensitive above, run \`git status\`, \`git diff\`, and \`git log\` against the base branch.`
- Capturar só o que existe na conversa (nada reproduzível de git); nunca mencionar commits, PRs, merges.

## File Structure

- `claude/skills/handoff/SKILL.md` — reescrito: detecção de modo, destino por branch, flag `--share`, invocar `save-session-learnings`.
- `claude/skills/handoff-continue/SKILL.md` — reescrito: ler por branch, branch sem handoff, migração de `HANDOFF.md` legado.
- `claude/skills/jira/SKILL.md` — passo de criação/atualização do task file passa a importar o handoff do comentário `## Handoff` mais recente.
- `claude/skills/jira-workflow/templates/task.md` — ganha a seção `## Handoff` com subseções.
- `claude/rules/workflow.md` — remove menção a `HANDOFF.md` da regra de split de docs.

---

## Task 1: Adicionar seção `## Handoff` ao template do task file

**Files:**
- Modify: `claude/skills/jira-workflow/templates/task.md`

**Interfaces:**
- Produces: seção `## Handoff` com as 6 subseções nomeadas, consumida pelas tarefas 2, 3 e 4.

- [ ] **Step 1: Inserir a seção `## Handoff` após `## Work log`**

Adicionar ao final de `claude/skills/jira-workflow/templates/task.md`:

```markdown

## Handoff

Written/updated by the `handoff` skill when stopping mid-task. Empty until first handoff.

### Why

Problem being solved, approach chosen, alternatives rejected.

### In Progress

Last step taken and intended next step at the moment of stopping.

### Open Questions / Hypotheses

Unresolved investigations and unconfirmed suspicions.

### Known Broken

Each item marked *intentional* or *unexpected*.

### How to Resume

A concrete first command.

### Next Steps

Concrete action items.
```

- [ ] **Step 2: Verificar**

Run: `grep -nE '^## Handoff|^### (Why|In Progress|Open Questions|Known Broken|How to Resume|Next Steps)$' claude/skills/jira-workflow/templates/task.md`
Expected: 1 linha `## Handoff` + 6 subseções listadas, todas após `## Work log`.

---

## Task 2: Reescrever `handoff/SKILL.md` (dual-mode + `--share`)

**Files:**
- Modify: `claude/skills/handoff/SKILL.md` (reescrita completa do corpo; manter frontmatter `name`/`description`)

**Interfaces:**
- Consumes: seção `## Handoff` do template (Task 1); convenção de paths do `jira-workflow`.
- Produces: comportamento de escrita por branch e comentário Jira `## Handoff` (consumido pela retomada nas tarefas 3 e 4).

- [ ] **Step 1: Substituir o corpo do SKILL por estas instruções**

Manter o frontmatter e reescrever o corpo assim:

````markdown
---
name: handoff
description: Use when ending a session, completing a milestone, or stopping mid-task and context must be preserved for the next agent
---

The handoff belongs to the **current branch**. Capture only what exists in the conversation; skip anything reproducible from git unless explicitly requested. Write imperatively and densely, no narration. Never mention git commits, PRs, or merges.

Accepts an optional `--share` flag (Jira mode only).

## 1. Detect mode

- **Jira mode** if `.jira/config.md` exists AND a task file exists for the current branch. Branch is `feature/<JIRA_ID>`; task file is `<jira_folder>/<JIRA_ID>.md` (resolve `<jira_folder>` from `.jira/config.md` → `## Paths`; default `.jira/`).
- **Local mode** otherwise. Target is `.handoff/<current-branch>.md`.

## 2. Invoke `save-session-learnings`

## 3. Read the existing handoff (if any) and carry forward

Read the current handoff (the `## Handoff` section of the task file in Jira mode, or `.handoff/<branch>.md` in local mode). Extract still-relevant **Open Questions / Hypotheses** and **Known Broken** items to carry forward.

## 4. Write the handoff

Write these subsections:
- **Why**: problem being solved, approach chosen, alternatives rejected.
- **In Progress**: last step taken and intended next step at the moment of stopping.
- **Open Questions / Hypotheses**: unresolved investigations and unconfirmed suspicions.
- **Known Broken**: each item marked *intentional* or *unexpected*.
- **How to Resume**: a concrete first command.
- **Next Steps**: concrete action items.

**Jira mode:** write into the `## Handoff` section of the task file (create the section from the template if missing). Leave `## Work log` untouched.

**Local mode:** write to `.handoff/<current-branch>.md` (create the folder if needed). The subsections above are `##` headings in this file. Then handle `.gitignore` opt-in: run `grep -xF '.handoff/' .gitignore`; if it doesn't match, suggest adding `.handoff/` to `.gitignore` and ask before making any change. Never add it without confirmation.

## 5. Append the footer line verbatim

> Before trusting anything time-sensitive above, run `git status`, `git diff`, and `git log` against the base branch.

## 6. `--share` (Jira mode only)

If `--share` was passed and in Jira mode, also publish a **new** comment on the issue via `mcp__atlassian__addCommentToJiraIssue` (`contentFormat: "markdown"`). The comment body starts with the fixed header `## Handoff` followed by the same subsections. Always a new comment — no upsert. If `--share` is passed in local mode, warn that there's no Jira issue to share to and skip.

## 7. Safety `/clear`

Double-check to ensure a safety `/clear` invocation.
````

- [ ] **Step 2: Verificar**

Run: `grep -nE 'current branch|\.handoff/|## Handoff|--share|save-session-learnings|grep -xF|git status.*git diff.*git log' claude/skills/handoff/SKILL.md`
Expected: casa detecção de modo, path local, marcador `## Handoff`, flag, invocação de learnings, opt-in do gitignore e a linha-rodapé.
Confirmar também que **não** existe mais escrita de `HANDOFF.md` na raiz: `grep -n 'HANDOFF.md' claude/skills/handoff/SKILL.md` → sem resultados.

---

## Task 3: Reescrever `handoff-continue/SKILL.md` (por branch + branch sem handoff + migração legada)

**Files:**
- Modify: `claude/skills/handoff-continue/SKILL.md` (reescrita completa do corpo; manter frontmatter)

**Interfaces:**
- Consumes: destino de handoff por branch definido na Task 2.

- [ ] **Step 1: Substituir o corpo do SKILL por estas instruções**

````markdown
---
name: handoff-continue
description: Read the current branch's handoff and continue from where we left off
---

Resume **your own** work on the current branch. (Resuming someone else's work from a Jira issue is the `/jira` flow, not this skill.)

## 1. Detect mode and locate the handoff

- **Jira mode** if `.jira/config.md` exists AND a task file exists for the current branch (`feature/<JIRA_ID>` → `<jira_folder>/<JIRA_ID>.md`). Handoff is the `## Handoff` section of that file.
- **Local mode** otherwise. Handoff is `.handoff/<current-branch>.md`.

## 2. Migrate a legacy root `HANDOFF.md`

If a `HANDOFF.md` exists at the project root, warn the user and ask whether to migrate it to the branch's handoff destination (the `## Handoff` section of the task file in Jira mode, or `.handoff/<branch>.md` in local mode). If confirmed, move its content there and delete the root `HANDOFF.md`. If declined, leave it and continue.

## 3. Handle a branch with no handoff

If no handoff exists for the current branch (and no legacy file was migrated), ask: "Nenhum handoff encontrado para `<branch>`. Continuar sem contexto de sessão anterior?" If yes, proceed as a first session on the branch and stop here. If no, stop.

## 4. Continue

Read the handoff. Identify the next task from **Next Steps** / **How to Resume**.

Suggest the best-fit model for the task.

Suggest the `mcp` command with the appropriate servers from `mcp --list`, one `--add` per line.

If on `main`, create a new branch whose name reflects the task being resumed.
````

- [ ] **Step 2: Verificar**

Run: `grep -nE 'current branch|\.handoff/|## Handoff|Nenhum handoff encontrado|HANDOFF.md|mcp --list' claude/skills/handoff-continue/SKILL.md`
Expected: casa leitura por branch, prompt de branch sem handoff (pt-BR verbatim), migração de `HANDOFF.md` legado e a sugestão de `mcp`.

---

## Task 4: Importar handoff do comentário Jira no `jira/SKILL.md`

**Files:**
- Modify: `claude/skills/jira/SKILL.md` (dentro de **Start task**, no passo de criação do task file)

**Interfaces:**
- Consumes: comentário `## Handoff` publicado pela Task 2 (`--share`); seção `## Handoff` do template (Task 1).

- [ ] **Step 1: Adicionar o passo de importação no fluxo Start task**

Em `claude/skills/jira/SKILL.md`, no bloco **Start task**, logo após o passo 2 (criar o task file), inserir um novo passo:

```markdown
2b. Import the latest handoff comment: search the issue's comments for the most recent one starting with the marker `## Handoff`. If found, write its subsections into the `## Handoff` section of the task file (create the section from the template if missing). Do not touch `## Work log`.
```

Renumerar os passos seguintes se necessário, ou usar `2b` como acima para evitar renumeração em cascata.

- [ ] **Step 2: Verificar**

Run: `grep -nE '## Handoff|most recent|handoff comment' claude/skills/jira/SKILL.md`
Expected: passo de importação presente no bloco Start task, referenciando o comentário `## Handoff` mais recente.

---

## Task 5: Remover menção a `HANDOFF.md` em `workflow.md`

**Files:**
- Modify: `claude/rules/workflow.md:10`

**Interfaces:** nenhuma.

- [ ] **Step 1: Reescrever a regra de split de docs sem `HANDOFF.md`**

Trocar a menção a `HANDOFF.md` por linguagem que cubra apenas docs cross-cutting versionados. A regra deve deixar claro que `.handoff/` e `.jira/` (opcionalmente git-ignored) não entram em PRs, então não precisam do split. Manter o resto da mecânica (branch irmã `chore/<id>-docs-*`, merge primeiro, reset + cherry-pick, backup ref).

Redação sugerida para o início da regra:

```markdown
- Keep feature PRs focused on the topic in the branch name. When status reports or other cross-cutting versioned docs accumulate on a `feat/*` branch, split them into a sister `chore/<same-id>-docs` branch from `main`, merge it first, then `git reset --hard origin/main` + cherry-pick the topical commits onto the feature branch and force-push. Create a `backup/<branch>-pre-cleanup` ref before destructive resets — the harness may block `--hard` against the feature branch otherwise. (Handoffs live under `.handoff/` or `.jira/`, git-ignored, so they never reach a PR.)
```

- [ ] **Step 2: Verificar**

Run: `grep -n 'HANDOFF.md' claude/rules/workflow.md`
Expected: sem resultados.

---

## Self-Review

**Spec coverage:**
- Modelo conceitual (branch corrente, dual-mode) → Task 2, Task 3.
- Formato `## Handoff` (6 subseções) → Task 1 (template), Task 2 (escrita).
- `--share` novo comentário a cada vez → Task 2 Step 1 §6.
- `.handoff/` gitignore opt-in → Task 2 Step 1 §4.
- Branch sem handoff (perguntar) → Task 3 §3.
- `HANDOFF.md` legado (migrar avisando) → Task 3 §2.
- Retomada por outro via `/jira` → Task 4.
- `workflow.md` sem `HANDOFF.md` → Task 5.

**Placeholder scan:** nenhum TBD/TODO; todas as instruções são conteúdo final.

**Type consistency:** marcador `## Handoff`, path `.handoff/<branch>.md`, subseções nomeadas e linha-rodapé usados idênticos em todas as tarefas.