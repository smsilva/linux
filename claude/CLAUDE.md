# Claude global instructions

<!-- Global instructions live in rules/*.md (symlinked to ~/.claude/rules/). This file is kept for the ~/.claude/CLAUDE.md symlink created by install.sh. -->

## Jira

Sempre que o usuário disser que vai **iniciar uma issue** (qualquer fraseado: "iniciar o
trabalho", "vou começar a X", "iniciar pela issue Y"), invocar a skill `jira` (`/jira <ID>`)
— ela atribui a issue, transiciona para "In Development" (ou "In Progress" se o workflow não
tiver esse status) e cria/troca para a branch `feat/<id-da-issue>` a partir da main.

Identificadores específicos (accountId, cloudId, issue-type ids, épicos, contexto de
projeto) vivem no `CLAUDE.local.md` do repositório onde o trabalho acontece.

Quando o usuário pedir para levar uma issue a um status específico (ex.: "coloca em In
Development", "leva pra In Production"), executar **todas** as transições
intermediárias necessárias em sequência até chegar lá — não parar na primeira. Re-
consultar `getTransitionsForJiraIssue` a cada passo (os transition IDs mudam por issue)
e seguir a cadeia de transições do workflow daquele projeto/tipo de issue (ver
`CLAUDE.local.md` do repositório para a cadeia específica, quando documentada).
