#!/bin/bash
CURRENT_USERNAME=$1

echo "Configuring /etc/sudoers.d/${CURRENT_USERNAME} sudoer file"

if [[ ! -e /etc/sudoers.d/${CURRENT_USERNAME} ]]; then
  echo "${CURRENT_USERNAME} ALL=(ALL) NOPASSWD: ALL" \
  | sudo tee /etc/sudoers.d/${CURRENT_USERNAME}
fi
