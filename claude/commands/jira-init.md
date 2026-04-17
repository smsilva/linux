Use a `jira-workflow` skill para as operações MCP.

Inicializa a configuração Jira do projeto atual, gerando `.claude/JIRA-PROJECT.md` com campos
obrigatórios descobertos via MCP. Deve ser executado uma vez por projeto.

## Passos

1. Se `.claude/JIRA-PROJECT.md` já existir, mostre o conteúdo e pergunte se deseja sobrescrever

2. Via MCP, em paralelo:
   - `getAccessibleAtlassianResources` → obter `cloudId` e URL base do site
   - `atlassianUserInfo` → obter nome do usuário logado

3. `getVisibleJiraProjects` → listar projetos disponíveis e pedir ao usuário que escolha um

4. Para o projeto escolhido:
   - `getJiraProjectIssueTypesMetadata` → listar tipos de issue
   - Para os tipos Story e Task: `getJiraIssueTypeMetaWithFields` → listar campos `required`
     e campos com `allowedValues` (custom fields potencialmente obrigatórios pelo board)

5. Perguntar ao usuário:
   - "Há labels obrigatórias para o board filtrar corretamente?" (ex: `Cloud_IDP`)
   - Para cada custom field não-óbvio descoberto: "O campo `<nome>` é obrigatório? Se sim, qual valor usar?"

6. Gerar `.claude/JIRA-PROJECT.md` com o formato abaixo

7. Perguntar: "Este arquivo deve ser commitado (config de equipe) ou adicionado ao `.gitignore` (config local)?"
   - Se local: adicionar `JIRA-PROJECT.md` ao `.gitignore`

## Formato de `.claude/JIRA-PROJECT.md`

```markdown
# Jira Project Config

**Project:** <PROJECT_KEY>
**Site:** <https://account.atlassian.net>
**Responsável:** <display name do usuário>

## Criação de issues — campos obrigatórios

Ao criar qualquer issue via `mcp__atlassian__createJiraIssue`, incluir em `additional_fields`:

```json
{
  "labels": ["<LABEL>"],
  "<customfield_xxxxx>": <valor>
}
```

> `<customfield_xxxxx>` — <nome do campo>: <por que é obrigatório, ex: "board filtra por este campo">

## Notas do board

<observações sobre filtros, sprints, epics, campos especiais>
```
