#!/bin/bash
set -e

INSTALL_DIR="${HOME}/tldr-fmt"

if [[ ! -e "${INSTALL_DIR}" ]]; then
  git clone git clone https://github.com/avih/tldr-fmt "${INSTALL_DIR}"
fi

if ! grep --quiet --extended-regexp "export PATH.*\/tldr-fmt" ~/.bashrc; then
cat <<EOF >> ~/.bashrc

export PATH=\$PATH:${INSTALL_DIR}
EOF
fi
