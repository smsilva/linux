Use a `jira-workflow` skill para todas as operações com o Jira (MCP, JIRA.md, comentários, transições, atribuições).

$ARGUMENTS — JIRA_ID (épico, história ou task)

## Navegação

- Se já existir o arquivo JIRA.md, leia o conteúdo para obter o JIRA_ID e contexto, e continue de onde paramos
- Obtenha a issue pelo JIRA_ID recebido
- Se for épico: liste as histórias associadas que ainda precisam ser trabalhadas e peça para escolher uma
- Se for história com tasks: liste as tasks pendentes e peça para escolher uma
- A issue final de trabalho deve ser uma task ou história sem subtarefas

## Arquivo JIRA.md

**História:** [JIRA_ID — Criar compositions para os tenants/spoke](https://organization.atlassian.net/browse/JIRA_ID)  
**Épico:** [JIRA_EPIC_ID — Construção da base de Network](https://organization.atlassian.net/browse/JIRA_EPIC_ID)  
**Link:** https://organization.atlassian.net/browse/JIRA_ID  
**Status:** In Development  
**Responsável:** Silvio Manoel da Silva  
**Branch:** feature/JIRA_ID
**Objetivo**: O que estamos tentando realizar com esta tarefa
**Progresso Atual**: O que foi feito até agora
**O que Funcionou**: Abordagens que tiveram sucesso e devem ser repetidas ou expandidas
**O que Não Funcionou**: Abordagens que falharam (para que não sejam repetidas)
**Próximos Passos**: Itens de ação claros para continuar

## Iniciar tarefa

1. Se não estiver atribuída, confirme e atribua ao usuário atual
2. Crie o JIRA.md se não existir
3. Faça checkout da main e puxe as últimas mudanças
4. Crie ou faça checkout da branch `feature/<JIRA_ID>`
5. Se a branch já existia remotamente, faça `git pull --rebase`
6. Faça rebase a partir da main para garantir atualização
7. Se o campo Sprint estiver vazio, pergunte se deseja adicionar a issue ao sprint atual e faça isso via MCP se confirmado
8. Adicione comentário: "Iniciando o trabalho nesta tarefa."
9. Transite o status para "Em Progresso"
