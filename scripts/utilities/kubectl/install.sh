#!/bin/bash

# Update and Get Google Cloud Apt Key
sudo apt-get update -qq && \
sudo curl --silent "https://packages.cloud.google.com/apt/doc/apt-key.gpg" | sudo apt-key add -

# Add Kubernetes Repository
cat <<EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF

# Update package list
sudo apt-get update -q

# Set Kubernetes Version
KUBERNETES_VERSION="$(apt-cache madison kubeadm | head -1 | awk '{ print $3 }')" && \
KUBERNETES_IMAGE_VERSION="${KUBERNETES_VERSION%-*}" && \
clear && \
echo "" && \
echo "KUBERNETES_VERSION.........: ${KUBERNETES_VERSION}" && \
echo "KUBERNETES_IMAGE_VERSION...: ${KUBERNETES_IMAGE_VERSION}" && \
echo ""

sudo apt-get install --yes -qq \
  kubectl="${KUBERNETES_VERSION}" | grep --invert-match --extended-regexp "^Hit|^Get|^Selecting|^Preparing|^Unpacking"
