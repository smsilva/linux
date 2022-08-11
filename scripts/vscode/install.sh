#!/bin/bash
set -e

if ! which code &> /dev/null; then
  sudo apt update

  sudo apt-get install --yes -q \
    software-properties-common \
    apt-transport-https \
    wget 

  wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc

  sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"

  sudo apt install code
fi
