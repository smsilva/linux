#!/bin/bash

# Install using native package management
# https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#install-using-native-package-management

if ! which kubectl > /dev/null; then
  sudo apt-get update -qq && \
  sudo apt-get install --yes \
    apt-transport-https \
    ca-certificates \
    curl

  # Get Google Cloud Apt Key
  curl \
    --fail \
    --silent \
    --show-error \
    --location \
    "https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key" \
  | sudo gpg \
    --dearmor \
    --output /etc/apt/keyrings/kubernetes-apt-keyring.gpg

  sudo chmod 644 /etc/apt/keyrings/kubernetes-apt-keyring.gpg

# Add Kubernetes Repository
cat <<EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /
EOF

  sudo apt-get update -qqq

  sudo apt-get install kubectl --yes -q
fi
