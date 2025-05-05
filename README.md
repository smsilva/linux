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

Para configurar qual chave usar, crie um arquivo `~/.ssh/config` com o conteúdo abaixo:

```bash
Host *
    User git
    PubkeyAcceptedAlgorithms +ssh-rsa
    HostkeyAlgorithms +ssh-rsa
    StrictHostKeyChecking no

Host github.com-pessoal
    HostName github.com
    IdentityFile ~/.ssh/id_ed25519

Host github.com
    HostName github.com
    IdentityFile ~/.ssh/id_rsa

Host ssh.dev.azure.com
    HostName ssh.dev.azure.com
    IdentityFile ~/.ssh/id_ed25519
```

## Configurando o repositório para usar a chave correta

```bash
git remote set-url origin git@github.com-pessoal:smsilva/linux.git
```
