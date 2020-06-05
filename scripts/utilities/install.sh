#!/bin/bash
set -e

sudo apt-get install -y \
  bat \
  cowsay \
  curl \
  fd-find \
  git \
  tmux \
  powerline \
  powerline-gitstatus \
  vim \
  wget \
  xclip

scripts/utilities/powerline/install.sh
scripts/utilities/tmux/install.sh
scripts/utilities/fuzzy-finder/install.sh
