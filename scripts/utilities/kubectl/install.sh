#!/bin/bash

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
    "https://packages.cloud.google.com/apt/doc/apt-key.gpg" \
  | sudo gpg \
    --dearmor \
    --output /etc/apt/keyrings/kubernetes-archive-keyring.gpg

# Add Kubernetes Repository
cat <<EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
deb [signed-by=/etc/apt/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main
EOF

  sudo apt-get update -qqq

  sudo apt-get install kubectl=1.27.4-00 --yes -q

  sudo apt-mark hold kubectl
fi
