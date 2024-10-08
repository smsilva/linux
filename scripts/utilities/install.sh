#!/bin/bash
sudo apt-get update -q

sudo apt-get upgrade --yes -qq

sudo apt-get install --yes -q \
  apt-transport-https \
  bat \
  cowsay \
  curl \
  fd-find \
  flameshot \
  fortune \
  gnupg \
  ipcalc \
  jq \
  libxml2-utils \
  nmap \
  powerline \
  powerline-gitstatus \
  tmux \
  translate-shell \
  tree \
  vim-gtk3 \
  wget \
  xclip

find scripts/utilities/ \
  -mindepth 1 \
  -maxdepth 1 \
  -type d \
| sort \
| while read FOLDER; do
  echo "============================================"
  echo "FOLDER.: ${FOLDER}"
  echo ""

  . ${FOLDER}/install.sh

  sleep 2
  echo ""
  echo ""
  echo ""
done
