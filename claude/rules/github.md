# GitHub

- The active `gh` account is the corporate one (`silvios_ciandt`, an Enterprise Managed User), which GitHub refuses on personal repositories (`smsilva/*`, such as `smsilva/linux`). For those, run `gh` with the personal account without switching the active account other sessions use: `GH_TOKEN="$(gh auth token --user smsilva)" gh pr create ...` (and `gh pr checks`, `gh pr merge --rebase --delete-branch` the same way); never print the token (2026-11-24).
