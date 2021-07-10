#!/bin/bash
echo "Configuring /etc/sudoers.d/${USER} sudoer file"

if [[ ! -e /etc/sudoers.d/${USER} ]]; then
  echo "${USER} ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/${USER}
fi
