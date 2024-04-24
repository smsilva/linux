#!/bin/bash
set -e

if [[ ! -e "${HOME}/.fzf" ]]; then
  git clone --depth 1 https://github.com/junegunn/fzf.git ${HOME}/.fzf
  
  "${HOME}/.fzf/install" --key-bindings --completion --update-rc
fi
