#!/bin/bash
set -e

git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf

#~/.fzf/install

cat <<EOF >> ~/.bashrc
export FZF_DEFAULT_COMMAND="fd --type f --follow --exclude .git"
export FZF_DEFAULT_OPTS="--height 40% --layout=reverse --border"
export FZF_CTRL_T_COMMAND="${FZF_DEFAULT_COMMAND}"
EOF
