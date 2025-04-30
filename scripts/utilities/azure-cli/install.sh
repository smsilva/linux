#!/bin/bash
if ! which az > /dev/null; then
  sudo apt-get install \
    ca-certificates \
    curl \
    apt-transport-https \
    lsb-release \
    gnupg --yes -qq

  sudo mkdir -p /etc/apt/keyrings

  curl \
    --silent \
    --location \
    --show-error \
    --url https://packages.microsoft.com/keys/microsoft.asc |
  gpg --dearmor |
  sudo tee /etc/apt/keyrings/microsoft.gpg > /dev/null

  sudo chmod go+r /etc/apt/keyrings/microsoft.gpg

  installed_distribution=$(lsb_release --codename --short 2> /dev/null)

  if [[ "${installed_distribution?}" == "noble" ]]; then
    installed_distribution="jammy"
  fi

  cat <<EOF | sudo tee /etc/apt/sources.list.d/azure-cli.list
deb [arch=`dpkg --print-architecture` signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/repos/azure-cli/ ${installed_distribution?} main
EOF

  sudo apt-get update -q
  sudo apt-get install azure-cli --yes
fi

az version --output yaml
