#!/bin/bash
ln --symbolic "${PWD}/scripts/utilities/tmux/tmux.conf" "${HOME}/.tmux.conf" &> /dev/null

# ~/.tmux.conf
if ! grep --quiet --extended-regexp "powerline.conf" ~/.tmux.conf; then
  sed '1i source /usr/share/powerline/bindings/tmux/powerline.conf' ~/.tmux.conf --in-place
fi
