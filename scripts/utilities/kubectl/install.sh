#!/bin/bash

if ! which kubectl > /dev/null; then
  sudo curl \
    --location \
    --output "/usr/share/keyrings/kubernetes-archive-keyring.gpg" \
    "https://packages.cloud.google.com/apt/doc/apt-key.gpg"

cat <<EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main
EOF

  sudo apt-get update -qqq

  sudo apt-get install kubectl=1.24.13-00 --yes -q

  sudo apt-mark hold kubectl
fi
