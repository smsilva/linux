# Claude global instructions

<!-- Global instructions live in rules/*.md (symlinked to ~/.claude/rules/). This file is kept for the ~/.claude/CLAUDE.md symlink created by install.sh. -->

## Jira

Quando o usuário pedir para "iniciar o trabalho" em uma issue Jira, automaticamente:

1. Atribuir a issue para `silvios@ciandt.com` (accountId: `5dcaf1e691a0610e03b81936`)
2. Transicioná-la para "In Development" caso ainda não esteja

## Contexto EMU dry-run

- **FLWP-66200 (D2):** concluída em 31/07/2026 — azure-login service principal validado, run 7 ID `30630728549`, todos os 3 elos passaram (github/token, docker-login, azure-login). Status: In Production.
- **Próxima story:** FLWP-66201 (D3)
