#!/bin/bash
set -e

echo ""
echo "Installing basic utilities..."
echo ""

sudo apt-get install --yes \
  apt-transport-https \
  bat \
  cowsay \
  curl \
  fd-find \
  fortune \
  git \
  ipcalc \
  jq \
  powerline \
  powerline-gitstatus \
  tmux \
  translate-shell \
  tree \
  vim-gtk3 \
  wget \
  xclip

find scripts/utilities/ -maxdepth 1 -type d | sed '1d' | while read FOLDER; do
echo ${FOLDER}/install.sh
done | sh
