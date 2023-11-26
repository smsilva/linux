#!/bin/bash
if ! which node > /dev/null; then
  sudo apt-get update
  sudo apt-get install --yes \
    ca-certificates \
    curl \
    gnupg
  sudo mkdir -p /etc/apt/keyrings
  curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key \
  | sudo gpg \
    --dearmor \
    --output /etc/apt/keyrings/nodesource.gpg

  NODE_MAJOR=20
  echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_MAJOR?}.x nodistro main" \
  | sudo tee /etc/apt/sources.list.d/nodesource.list

  sudo apt-get update
  sudo apt-get install nodejs -y
fi

node --version

if which npm > /dev/null; then

  if ! which cz > /dev/null; then
    sudo npm install -g commitizen
  fi

  if ! which tldr &> /dev/null; then
    sudo npm install -g tldr
  fi
fi
