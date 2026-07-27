# Handoff por-branch, dual-mode, integrado ao Jira — spec

**Status:** spec final (pronta para `writing-plans`)
**Data:** 2026-07-24 (fechada 2026-07-27)
**Alvo:** refatorar `claude/skills/handoff/SKILL.md`, `claude/skills/handoff-continue/SKILL.md`,
`claude/skills/jira/SKILL.md` e `claude/rules/workflow.md`

## Problema

O `handoff` atual escreve um único `HANDOFF.md` na raiz do projeto. Numa equipe onde
vários membros trabalham no mesmo repositório, se cada um roda o próprio handoff, todos
disputam o mesmo arquivo. O que funciona e deve ser preservado: **saber onde paramos e
ter contexto denso para o próximo agente** — não o arquivo em si.

## Contexto descoberto

- A equipe usa Jira via MCP Atlassian.
- O skill `jira` / `jira-workflow` **já mantém um arquivo por-task** em
  `<jira_folder>/<JIRA_TASK_ID>.md` (default `.jira/`) e **já o sincroniza como comentário
  no Jira** em momentos-chave — incluindo *"closing out the work (handoff or completion)"*.
- O skill `jira` resolve JIRA_ID a partir da URL/ID, faz fetch, recria o task file local,
  cria/checkout da branch `feature/<JIRA_ID>` e transiciona para In Progress.
- Branch no modo Jira é sempre `feature/<JIRA_ID>`.

## Modelo conceitual (confirmado)

**Regra única:** o handoff pertence à **branch corrente**.

- **Com Jira** (branch `feature/<JIRA_ID>` e `.jira/<JIRA_ID>.md` existe): handoff vive
  numa seção `## Handoff` dentro do task file.
- **Sem Jira** (POC/projeto pessoal): handoff vive em `.handoff/<branch>.md`.

Elimina o `HANDOFF.md` único na raiz e a colisão entre membros.

Detecção de modo (trivial): existe `.jira/config.md` e um task file para a branch
corrente? → modo Jira. Senão → modo local.

## Decisões fechadas

1. **Modelo conceitual** — confirmado (handoff pertence à branch corrente).

2. **Formato da seção `## Handoff`** — as mesmas subseções do `HANDOFF.md` atual:
   `Why`, `In Progress`, `Open Questions / Hypotheses`, `Known Broken`, `How to Resume`,
   `Next Steps`. No modo Jira, essas subseções ficam sob o cabeçalho `## Handoff` do task
   file (coexistem com `## Work log`, não o substituem).

3. **`--share` no modo Jira** — publica um **novo comentário a cada vez** (marcador
   `## Handoff` no início). Na retomada, sempre usar o **comentário mais recente** com
   esse marcador. Sem upsert.

4. **`.handoff/` no `.gitignore`** — **opt-in**, mesmo comportamento do `jira-workflow`
   com `.jira/`: o skill roda `grep -xF '.handoff/' .gitignore`; se não casar, sugere
   adicionar e pergunta antes de mexer. Nunca adiciona sem confirmação.

5. **`handoff-continue` sem handoff para a branch** — perguntar ao usuário:
   *"Nenhum handoff encontrado para `<branch>`. Continuar sem contexto de sessão
   anterior?"*. Se sim, comporta-se como primeira sessão na branch.

6. **`HANDOFF.md` legado na raiz** — o `handoff-continue` detecta, **avisa**, pergunta se
   migra o conteúdo para o destino novo (`.jira/<ID>.md` seção `## Handoff`, ou
   `.handoff/<branch>.md`), e ao confirmar move o conteúdo e deleta o original.

7. **Retomada por outro membro = fluxo do `/jira`** — ao recriar o task file, o `/jira`
   busca o comentário mais recente com marcador `## Handoff` e o importa para a seção
   `## Handoff` do task file. Sem comando novo.

8. **`workflow.md`** — remover a menção a `HANDOFF.md` da regra de split de docs. Como
   `.handoff/` e `.jira/` são (opcionalmente) git-ignored, não aparecem em PRs. A regra
   permanece para status reports e outros docs cross-cutting versionados.

## Responsabilidades por skill

- **`handoff`** — escreve o handoff pertencente à branch corrente:
  - modo Jira → seção `## Handoff` do task file;
  - modo local → `.handoff/<branch>.md`;
  - com `--share` (só modo Jira) → também publica novo comentário `## Handoff` no Jira.
- **`handoff-continue`** — retomada **própria**: deriva da branch corrente, lê o handoff
  correspondente, continua. Trata branch sem handoff (decisão 5) e `HANDOFF.md` legado
  (decisão 6).
- **`jira`** — retomada **por outro**: ao recriar o task file, importa o handoff do
  comentário `## Handoff` mais recente (decisão 7).

## Conteúdo do handoff (preservar do skill atual)

Subseções: `Why`, `In Progress`, `Open Questions / Hypotheses`, `Known Broken`,
`How to Resume`, `Next Steps`. Mais:
- invocar `save-session-learnings` no início;
- ao reescrever, carregar adiante `Open Questions` / `Known Broken` ainda relevantes;
- linha-rodapé verbatim:
  *"Before trusting anything time-sensitive above, run `git status`, `git diff`, and
  `git log` against the base branch."*;
- capturar só o que existe na conversa (nada reproduzível de git); nunca mencionar
  commits, PRs, merges.

## Arquivos afetados

- `claude/skills/handoff/SKILL.md` — reescrever: detecção de modo, destino por branch,
  flag `--share`.
- `claude/skills/handoff-continue/SKILL.md` — reescrever: ler por branch, branch sem
  handoff, migração de `HANDOFF.md` legado.
- `claude/skills/jira/SKILL.md` — no passo "Create/update task file", importar handoff do
  comentário `## Handoff` mais recente.
- `claude/skills/jira-workflow/templates/task.md` — decidir na implementação se a seção
  `## Handoff` entra no template ou é adicionada pelo skill sob demanda.
- `claude/rules/workflow.md` — remover menção a `HANDOFF.md`.

## Próximo passo

Invocar `writing-plans` para transformar esta spec em plano de implementação por tarefas.