#!/bin/bash
set -e

if ! which az > /dev/null; then
  curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

  sudo apt-get update

  sudo apt-get install \
    ca-certificates \
    curl \
    apt-transport-https \
    lsb-release \
    gnupg

  sudo mkdir -p /etc/apt/keyrings

  curl -sLS https://packages.microsoft.com/keys/microsoft.asc |
    gpg --dearmor |
    sudo tee /etc/apt/keyrings/microsoft.gpg > /dev/null

  sudo chmod go+r /etc/apt/keyrings/microsoft.gpg

  INSTALLED_DISTRIBUTION=$(lsb_release --codename --short 2> /dev/null)
  cat <<EOF | sudo tee /etc/apt/sources.list.d/azure-cli.list
deb [arch=`dpkg --print-architecture` signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/repos/azure-cli/ ${INSTALLED_DISTRIBUTION?} main
EOF

  sudo apt-get update -q
  sudo apt-get install azure-cli
fi
