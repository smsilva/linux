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

  node_major=20

  cat <<EOF | sudo tee /etc/apt/sources.list.d/nodesource.list
deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${node_major?}.x nodistro main
EOF

  sudo apt-get update -q
  sudo apt-get install nodejs -y -q
fi

node --version

if which npm > /dev/null; then
  mkdir -p ${HOME}/.npm-packages

  npm config set prefix "${HOME}/.npm-packages"

  if ! which tldr &> /dev/null; then
    npm install -g tldr
  fi
fi
