#!/bin/bash

kubectl_version="1.35"
kubernetes_apt_keyring="/etc/apt/keyrings/kubernetes-apt-keyring.gpg"

# Install using native package management
# https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#install-using-native-package-management

if ! which kubectl > /dev/null; then
  sudo apt-get update -qq && \
  sudo apt-get install --yes \
    apt-transport-https \
    ca-certificates \
    curl

    if [ -f "${kubernetes_apt_keyring?}" ]; then
      sudo rm -f ${kubernetes_apt_keyring?}
    else
      sudo mkdir -p /etc/apt/keyrings
    fi

  # Get Google Cloud Apt Key
  curl \
    --fail \
    --silent \
    --show-error \
    --location \
    "https://pkgs.k8s.io/core:/stable:/v${kubectl_version?}/deb/Release.key" \
  | sudo gpg \
    --dearmor \
    --output "${kubernetes_apt_keyring?}"

  sudo chmod 644 "${kubernetes_apt_keyring?}"

  # Add Kubernetes Repository
  cat <<EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
deb [signed-by=${kubernetes_apt_keyring?}] https://pkgs.k8s.io/core:/stable:/v${kubectl_version?}/deb/ /
EOF

  sudo apt-get update -qq

  last_available_kubectl_version=$(
    apt-cache madison kubectl \
      | grep pkgs.k8s.io \
      | awk '{ print $3 }' \
      | sort --version-sort \
      | tail -1
  )

  sudo apt-get install kubectl=${last_available_kubectl_version?} --yes -q

  sudo apt-mark hold kubectl
fi
