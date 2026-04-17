Use a `jira-workflow` skill para todas as operações com o Jira (MCP, JIRA.md, comentários, transições, atribuições).

$ARGUMENTS — JIRA_ID (épico, história ou task)

Se `.claude/JIRA-PROJECT.md` existir, leia-o antes de qualquer ação para obter as configurações
do projeto: URL do site, campos obrigatórios ao criar issues, labels, nome do responsável.
Se não existir, sugira rodar `/jira-init` para configurar o projeto.

## Navegação

- Se `$ARGUMENTS` estiver vazio e existir JIRA.md, leia o conteúdo para obter o JIRA_ID e contexto, e continue de onde paramos
- Se `$ARGUMENTS` estiver vazio e não existir JIRA.md, peça o JIRA_ID ao usuário
- Obtenha a issue pelo JIRA_ID recebido
- Se for épico: liste as histórias associadas que ainda precisam ser trabalhadas e peça para escolher uma
- Se for história:
    - liste as tasks pendentes e peça para escolher uma
    - se não tiver tasks pendentes, liste todas as tasks com os respectivos status e último comentário, e peça para escolher uma
- A issue final de trabalho deve ser uma task

## Arquivo JIRA.md

**Task:** [JIRA_TASK_ID — título da task](<JIRA_SITE_URL>/browse/JIRA_TASK_ID)
**História:** [JIRA_STORY_ID — título da história](<JIRA_SITE_URL>/browse/JIRA_STORY_ID)
**Épico:** [JIRA_EPIC_ID — título do épico](<JIRA_SITE_URL>/browse/JIRA_EPIC_ID)
**Status:** In Development
**Responsável:** <nome do usuário atual>
**Branch:** feature/JIRA_TASK_ID
**Objetivo**: O que estamos tentando realizar com esta tarefa
**Progresso Atual**: O que foi feito até agora
**O que Funcionou**: Abordagens que tiveram sucesso e devem ser repetidas ou expandidas
**O que Não Funcionou**: Abordagens que falharam (para que não sejam repetidas)
**Próximos Passos**: Itens de ação claros para continuar

## Iniciar tarefa

1. Se não estiver atribuída, confirme e atribua ao usuário atual
2. Crie o JIRA.md se não existir
3. Se a branch `feature/<JIRA_TASK_ID>` **não existir**:
   - Faça checkout da main e puxe as últimas mudanças
   - Crie a branch a partir da main: `git checkout -b feature/<JIRA_TASK_ID>`
4. Se a branch `feature/<JIRA_TASK_ID>` **já existir** (local ou remota):
   - Faça checkout da branch
   - Faça `git pull --rebase` se existir rastreamento remoto
5. Se o campo Sprint estiver vazio, pergunte se deseja adicionar a issue ao sprint atual e faça isso via MCP se confirmado
6. Adicione comentário: "Iniciando o trabalho na branch `feature/<JIRA_TASK_ID>`."
7. Transite o status para "Em Progresso"
