#!/bin/bash
if ! which docker &> /dev/null; then
  sudo apt-get remove \
    docker \
    docker-engine \
    docker.io \
    containerd runc

  sudo apt-get update -q

  sudo apt-get install -q \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common \
    --yes

  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

  sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"

  sudo apt-get update -q

  sudo apt-get install -q \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    --yes

  sudo usermod -aG docker ${USER}

  sudo systemctl enable docker
  sudo systemctl start docker
fi
