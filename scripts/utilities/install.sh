#!/bin/bash
set -e

sudo apt-get install -y \
  bat \
  cowsay \
  curl \
  fd-find \
  fortune \
  git \
  tmux \
  powerline \
  powerline-gitstatus \
  translate-shell \
  vim \
  wget \
  xclip

scripts/utilities/powerline/install.sh
scripts/utilities/tmux/install.sh
scripts/utilities/fuzzy-finder/install.sh

if ! grep --quiet --extended-regexp "today-fortune" ~/.bashrc; then
cat <<EOF >> ~/.bashrc

today-fortune
EOF
fi
