#!/bin/bash
cp scripts/utilities/tmux/tmux.conf ~/.tmux.conf

# ~/.tmux.conf
if ! grep --quiet --extended-regexp "powerline.conf" ~/.tmux.conf; then
  sed '1i source /usr/share/powerline/bindings/tmux/powerline.conf' ~/.tmux.conf --in-place
fi
