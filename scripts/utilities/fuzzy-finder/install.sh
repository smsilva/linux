#!/bin/bash
set -e

if [ ! -e ~/.fzf ]; then
  git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
  
  ~/.fzf/install --key-bindings --completion --update-rc
fi
