#!/bin/bash
set -e

sudo apt-get install -y \
  batcat \
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

powerline/install.sh
tmux/install.sh
