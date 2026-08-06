# Claude global instructions

<!-- Global instructions live in rules/*.md (symlinked to ~/.claude/rules/). This file is kept for the ~/.claude/CLAUDE.md symlink created by install.sh. -->

## Jira

Quando o usuário pedir para "iniciar o trabalho" em uma issue Jira, automaticamente:

1. Atribuir a issue para `silvios@ciandt.com` (accountId: `5dcaf1e691a0610e03b81936`)
2. Transicioná-la para "In Development" caso ainda não esteja

## Contexto EMU dry-run

- **Épico FLWP-66196** (cloudId Jira `a293ae84-29b1-4838-ba47-b8f890959f53`). Status por story vive no `CLAUDE.md` do projeto `flow-cloud-hub`, não aqui.
- **D6 (FLWP-66204):** concluída em 05/08/2026, In Production.
- **Próxima story ativa:** D5 (FLWP-66203) — bloqueio externo: owner precisa elevar `cloud-ao` para `organization_secrets: write`.
- **Cadeia de transições Jira até In Production** (workflow destas stories): `Finish Development` → `Start Testing` → `Finish Testing` → `Em homologação` → `Homologado` → `Move to Production`. Sempre re-consultar os transition IDs por story (mudam) via `getTransitionsForJiraIssue`.
