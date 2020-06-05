# Configuração Inicial com minhas preferências para o Ubuntu 20.04

Estes scripts instalam e configuram:

- Aliases para comandos como gcor que faz um git checkout de uma branch remota usando Fuzzy Finder (galias mostras os alias relacionados ao Git)
- Cria um link simbólico em ${HOME}/bin-${USER} apontandos para o diretório onde este repositório foi baixado/scripts/bin
- Configura o usuário atual como sudoer criando um arquivo em /etc/sudoers.d/${USER}
- Instala os seguintes utilitários:
  - bat
  - cowsay
  - curl
  - fd-find
  - fortune
  - git
  - tmux (cria um arquivo ~/.tmux.conf)
  - powerline (cria um arquivo ~/.config/powerline/config.json e altera o ~/.bashrc)
  - powerline-gitstatus
  - translate-shell
  - vim
  - wget
  - xclip
- Instala o Fuzzy Finder
