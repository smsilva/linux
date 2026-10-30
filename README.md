# Configuração Inicial com minhas preferências para o Ubuntu 24.04

Estes scripts instalam e configuram:

- Aliases para comandos como `gcor` que faz um `git checkout` de uma branch remota usando Fuzzy Finder (`galias` mostras os alias relacionados ao Git).

- Cria um link simbólico em `${HOME}/bin-${USER}` apontandos para o `ONDE_ESTE_REPOSITORIO_FOI_BAIXADO/scripts/bin`.

- Configura o usuário atual como sudoer criando um arquivo em `/etc/sudoers.d/${USER}`.

- Instala os seguintes utilitários:
  - apt-transport-https
  - bat
  - cowsay
  - curl
  - fd-find
  - fortune
  - gnupg
  - htop
  - ipcalc
  - iptraf
  - jq
  - libxml2-utils
  - nmap
  - powerline (cria um arquivo `${HOME}/.config/powerline/config.json` e altera o `${HOME}/.bashrc`)
  - powerline-gitstatus - tmux (cria um arquivo `${HOME}/.tmux.conf`)
  - tmux
  - translate-shell
  - tree
  - vim-gtk3
  - wget
  - xclip

- Instala o Fuzzy Finder

## Exemplo de Terminal com TMUX e Powerline configurados
![Terminal Configurado](/imagens/terminal.png)

## Configurando SSH Key

Para cria uma a chave SSH, execute o comando abaixo de acordo com o tipo de chave que você deseja criar:

### Chave Ed25519

```bash
ssh-keygen -t ed25519 -C "address@example.com" -f ~/.ssh/id_ed25519
```

### Chave RSA

```bash
ssh-keygen -t rsa -C "address@example.com" -f ~/.ssh/id_rsa
```

## Iniciar o ssh-agent

```bash
eval "$(ssh-agent -s)"
```

## Adicionar as chaves SSH ao ssh-agent

```bash
ssh-add ~/.ssh/id_ed25519
ssh-add ~/.ssh/id_rsa
```

## Configurando qual chave usar

Para configurar qual chave usar, crie um arquivo `~/.ssh/config` (modo `600`) com o conteúdo abaixo:

```bash
Host github.com
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
```

O `IdentitiesOnly yes` faz o ssh oferecer só essa chave. Sem ele, o ssh-agent oferece todas as que carrega, em ordem variável, e o GitHub autentica com a primeira que reconhece: quando é uma deploy key (por exemplo `ci: smsilva/azure-kubernetes`), a sessão vira a daquele repositório, e um repositório privado de outra conta ou organização responde `Permission denied (publickey)` de forma intermitente. Para conferir, `ssh -T git@github.com` deve responder sempre `Hi smsilva!`.

Uma deploy key, quando precisar ser usada, ganha um alias próprio com o seu `IdentityFile` e `IdentitiesOnly yes` (veja o alias abaixo), nunca o `github.com`. Não use `StrictHostKeyChecking no`: aceitar qualquer host key abre espaço para um man-in-the-middle.

## Alias curto para a conta pessoal (proposta)

Em vez de `github.com-personal`, usar um alias curto como `gh`. O `IdentitiesOnly yes` impede que o ssh-agent ofereça outra chave antes (o que autenticaria na conta errada), dispensando `GIT_SSH_COMMAND` e `core.sshCommand`:

```bash
Host gh
    HostName github.com
    IdentityFile ~/.ssh/id_rsa_personal
    IdentitiesOnly yes
```

Como o `Host *` já define `User git`, o clone fica:

```bash
git clone gh:wasp-foundry/agent-coordinator.git
```

Para migrar um repositório já clonado:

```bash
git remote set-url origin gh:wasp-foundry/agent-coordinator.git
```

Outras opções de nome: `me`, `pessoal`, `smsilva`. Para a conta do trabalho, algo como `gh-work`.

## Configurando o repositório para usar a chave correta

```bash
git remote set-url origin git@github.com-pessoal:smsilva/linux.git
```
