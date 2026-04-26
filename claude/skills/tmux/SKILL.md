---
name: tmux
description: Use when the user asks about tmux commands, shortcuts, sessions, windows, panes, copy mode, or how to manage terminal multiplexer layouts.
---

# tmux

Referência rápida de comandos tmux. Prefixo padrão: `Ctrl+b`.

## Sessions

| Ação | Comando |
|------|---------|
| Nova sessão | `tmux new -s nome` |
| Listar sessões | `tmux ls` |
| Attach | `tmux attach -t nome` |
| Detach | `Prefix d` |
| Matar sessão | `tmux kill-session -t nome` |
| Renomear sessão | `Prefix $` |
| Navegar entre sessões | `Prefix (` / `Prefix )` |

## Windows

| Ação | Comando |
|------|---------|
| Nova window | `Prefix c` |
| Listar windows | `Prefix w` |
| Próxima / anterior | `Prefix n` / `Prefix p` |
| Ir para window N | `Prefix N` |
| Renomear window | `Prefix ,` |
| Fechar window | `Prefix &` |
| Mover window para posição N | `tmux move-window -t :N` |

## Panes

| Ação | Comando |
|------|---------|
| Split horizontal | `Prefix "` |
| Split vertical | `Prefix %` |
| Navegar entre panes | `Prefix ←↑↓→` |
| Fechar pane | `Prefix x` |
| Zoom (toggle fullscreen) | `Prefix z` |
| Mostrar números dos panes | `Prefix q` |
| Redimensionar | `Prefix Ctrl+←↑↓→` |
| Rotacionar panes | `Prefix }` / `Prefix {` |
| Converter pane em nova window | `Prefix !` ou `tmux break-pane` |
| Mover pane para window N | `tmux break-pane -t :N` |
| Trazer pane de outra window | `tmux join-pane -s :W.P` |
| Mover sem mudar foco | adicionar flag `-d` |

### Exemplos: break-pane / join-pane

```bash
# Mover pane atual para window 2 (cria se não existir)
tmux break-pane -t :2

# Mover para nova window sem mudar o foco
tmux break-pane -d -t :2

# Trazer pane 0 da window 2 para a window atual
tmux join-pane -s :2.0

# Mesmo sem mudar foco
tmux join-pane -d -s :2.0
```

## Copy Mode

| Ação | Comando |
|------|---------|
| Entrar | `Prefix [` |
| Sair | `q` |
| Pesquisar para trás | `/` |
| Iniciar seleção | `Space` |
| Copiar seleção | `Enter` |
| Colar | `Prefix ]` |
| Scroll | `PgUp` / `PgDn` ou `Ctrl+u` / `Ctrl+d` |

## Utilitários

```bash
# Listar teclas configuradas
tmux list-keys

# Recarregar config sem reiniciar
tmux source-file ~/.tmux.conf
# ou dentro do tmux:
Prefix : source-file ~/.tmux.conf

# Mostrar opções de sessão
tmux show-options -g

# Sincronizar entrada em todos os panes da window
Prefix : setw synchronize-panes on
```

## Atalhos no modo comando (Prefix :)

```
new-window -n nome
split-window -h          # split vertical
split-window -v          # split horizontal
select-pane -t :.+       # próximo pane
swap-pane -s :1.0 -t :2.0
```
