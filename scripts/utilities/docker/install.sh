#!/bin/bash
if ! which docker &> /dev/null; then
  sudo apt-get remove \
    containerd \
    docker \
    docker-compose-plugin \
    docker-engine \
    docker.io \
    runc &> /dev/null

  sudo apt-get update -qq

  sudo apt-get install -qq \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common \
    --yes

  sudo install -m 0755 -d /etc/apt/keyrings

  curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  
  sudo chmod a+r /etc/apt/keyrings/docker.gpg

  echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

  sudo apt-get update -qq

  sudo apt-get install -qq \
    containerd.io \
    docker-buildx-plugin \
    docker-ce \
    docker-ce-cli \
    docker-compose-plugin \
    --yes

  sudo usermod -aG docker ${USER}

  sudo systemctl enable docker
  sudo systemctl start docker
fi
