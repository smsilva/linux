---
name: jira-workflow
description: Primitivas para interagir com o Jira via MCP Atlassian — configurar MCP, criar/atualizar JIRA.md, comentar, transicionar status e atribuir issues.
---

# jira-workflow

## 1. Verificar e configurar o MCP Atlassian

Verifique se o MCP Atlassian está ativo listando os servidores MCP disponíveis na conversa atual.

Se não estiver ativo, execute:

```
claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/mcp
```

Configure o projeto local para que o Claude não precise perguntar sobre qualquer ação de consulta ou lista usando o MCP Atlassian.

Exemplo:

`.claude/settings.local.json`:

```json
{
"permissions": {
    "allow": [
      "mcp__atlassian__atlassianUserInfo",
      "mcp__atlassian__getJiraIssue",
      "mcp__atlassian__getAccessibleAtlassianResources",
      "mcp__atlassian__searchJiraIssuesUsingJql",
      "mcp__atlassian__search",
      "mcp__atlassian__getTransitionsForJiraIssue",
      "mcp__atlassian__getConfluencePage",
      "mcp__atlassian__getConfluenceSpaces",
      "mcp__atlassian__getPagesInConfluenceSpace",
      "mcp__atlassian__getConfluencePageDescendants",
      "mcp__atlassian__getConfluencePageFooterComments",
      "mcp__atlassian__getConfluencePageInlineComments",
      "mcp__atlassian__getConfluenceCommentChildren",
      "mcp__atlassian__getVisibleJiraProjects",
      "mcp__atlassian__getJiraProjectIssueTypesMetadata",
      "mcp__atlassian__getJiraIssueTypeMetaWithFields",
      "mcp__atlassian__getIssueLinkTypes",
      "mcp__atlassian__getJiraIssueRemoteIssueLinks",
      "mcp__atlassian__lookupJiraAccountId",
      "mcp__atlassian__fetch",
      "mcp__atlassian__searchConfluenceUsingCql"
    ]
  }
}
```

## 2. Obter recursos acessíveis e usuário atual

Use `mcp__atlassian__getAccessibleAtlassianResources` para obter o `cloudId` do site Atlassian.
Guarde como `cloud_id` para uso em todas as chamadas MCP seguintes.

Use `mcp__atlassian__atlassianUserInfo` para obter o `accountId` do usuário logado.
Guarde como `current_user_account_id` para uso nas demais operações.

## 3. Buscar a issue

Use `mcp__atlassian__getJiraIssue` com `responseContentFormat: "markdown"` para obter os dados da issue.

Extraia os campos necessários para popular o JIRA.md:
- `key`, `summary`, `status`, `description`, `assignee`, `sprint`, `epic`

## 4. Criar ou atualizar JIRA.md

O arquivo `JIRA.md` deve existir na raiz do repositório **somente na branch de trabalho**.

Verifique se `JIRA.md` está no `.gitignore` do repositório. Se não estiver, adicione.

```markdown
# <ISSUE_KEY>: <summary>

**Status:** <status>
**Link:** <URL da issue no Jira>
**Assignee:** <nome do responsável>
**Sprint:** <sprint atual> *(opcional)*
**Epic:** <épico> *(opcional)*

## Descrição

<description>
```

Sincronize o conteúdo do JIRA.md como comentário na issue nos seguintes momentos:
- Ao criar o JIRA.md pela primeira vez
- Ao transicionar o status da issue
- Ao encerrar o trabalho (handoff ou conclusão)

## 5. Adicionar comentário

Use `mcp__atlassian__addCommentToJiraIssue` com `contentFormat: "markdown"`.

## 6. Transicionar status

1. Use `mcp__atlassian__getTransitionsForJiraIssue` para listar as transições disponíveis.
2. Identifique o ID da transição desejada pelo nome (ex: "Em Progresso").
3. Use `mcp__atlassian__transitionJiraIssue` com o `transition.id` encontrado.
4. Atualize o campo `Status` no JIRA.md e sincronize como comentário na issue.

## 7. Atribuir issue ao usuário atual

Use `mcp__atlassian__editJiraIssue` com:

```json
{
  "fields": {
    "assignee": { "accountId": "<current_user_account_id>" }
  }
}
```
