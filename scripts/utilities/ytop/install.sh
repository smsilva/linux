#!/bin/bash
set -e

VERSION="0.6.2"
INSTALL_DIR="${HOME}/bin/"

if ! [ -e "${INSTALL_DIR}" ]; then
  TAR_FILE="ytop-${VERSION}-x86_64-unknown-linux-gnu.tar.gz"
  
  wget "https://github.com/cjbassi/ytop/releases/download/0.6.2/${TAR_FILE}"
  
  [ ! -e "${INSTALL_DIR}" ] && mkdir "${INSTALL_DIR}"
  
  tar xvf "${TAR_FILE}" && \
  mv ytop "${INSTALL_DIR}" && \
  rm "${TAR_FILE}"
  
  mkdir -p ~/.config/ytop/
  
  cp scripts/utilities/ytop/monokai.json ~/.config/ytop/monokai.json
fi
