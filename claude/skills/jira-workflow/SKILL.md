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

## 2. Obter usuário atual

Use `mcp__atlassian__atlassianUserInfo` para obter o `accountId` do usuário logado.
Guarde como `current_user_account_id` para uso nas demais operações.

## 3. Criar ou atualizar JIRA.md

O arquivo `JIRA.md` deve existir na raiz do repositório **somente na branch de trabalho**.
Nunca deve ser commitado na main — garanta que está no `.gitignore` ou que será removido antes do merge.

Conteúdo mínimo:

```markdown
# <ISSUE_KEY>: <summary>

**Status:** <status>
**Link:** <URL da issue no Jira>

## Descrição

<description>
```

Atualize o campo `Status` sempre que transicionar a issue.

## 4. Adicionar comentário

Use `mcp__atlassian__addCommentToJiraIssue` com `contentFormat: "markdown"`.

## 5. Transicionar status

1. Use `mcp__atlassian__getTransitionsForJiraIssue` para listar as transições disponíveis.
2. Identifique o ID da transição desejada pelo nome (ex: "Em Progresso").
3. Use `mcp__atlassian__transitionJiraIssue` com o `transition.id` encontrado.

## 6. Atribuir issue ao usuário atual

Use `mcp__atlassian__editJiraIssue` com:

```json
{
  "fields": {
    "assignee": { "accountId": "<current_user_account_id>" }
  }
}
```
