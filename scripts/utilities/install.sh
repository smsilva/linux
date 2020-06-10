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

find scripts/utilities/ -maxdepth 1 -type d | sed '1d' | while read FOLDER; do
echo ${FOLDER}/install.sh
done | sh
