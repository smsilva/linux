#!/bin/bash
set -e

if ! which ytop &> /dev/null; then
  VERSION=$(curl --silent "https://api.github.com/repos/cjbassi/ytop/releases/latest" | grep '"tag_name"' | sed -E 's/.*"([^"]+)".*/\1/')

  INSTALL_DIR="${HOME}/bin/"

  TAR_FILE="ytop-${VERSION?}-x86_64-unknown-linux-gnu.tar.gz"
  
  wget "https://github.com/cjbassi/ytop/releases/download/${VERSION}/${TAR_FILE}"
  
  [ ! -e "${INSTALL_DIR}" ] && mkdir "${INSTALL_DIR}"
  
  tar xvf "${TAR_FILE}" && \
  mv ytop "${INSTALL_DIR}" && \
  rm "${TAR_FILE}"
  
  mkdir -p ~/.config/ytop/
  
  cp scripts/utilities/ytop/monokai.json ~/.config/ytop/monokai.json
fi
