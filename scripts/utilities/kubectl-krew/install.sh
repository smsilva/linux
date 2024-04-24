#!/bin/bash
INSTALL_DIR="${HOME}/.krew"

if [[ ! -e "${INSTALL_DIR?}" ]]; then
  (
    set -x; cd "$(mktemp -d)" &&
    curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/download/v0.4.4/krew-linux_amd64.tar.gz" &&
    tar zxvf krew-linux_amd64.tar.gz &&
    KREW=./krew-"$(uname | tr '[:upper:]' '[:lower:]')_amd64" &&
    "${KREW}" install krew
  )
fi

if ! grep --quiet --extended-regexp "^export.*KREW_ROOT.*PATH" ~/.bashrc; then
  echo 'export PATH="${KREW_ROOT:-${HOME}/.krew}/bin:${PATH}"' >> ~/.bashrc

  kubectl krew update

  kubectl krew install \
    ctx \
    ns \
    neat
fi
