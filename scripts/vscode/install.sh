#!/bin/bash
if ! which code &> /dev/null; then
  sudo apt-get update -q

  sudo apt-get install --yes -qq \
    software-properties-common \
    apt-transport-https \
    wget 

  wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc

  sudo add-apt-repository --yes "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"

  sudo apt-get install code --yes -q
fi
