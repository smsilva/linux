#!/bin/bash
if ! which yq > /dev/null; then
  VERSION="4.33.3"
  BINARY="yq_linux_amd64"
  TAR_FILE="${BINARY?}.tar.gz"

  echo "VERSION..: ${VERSION}"
  echo "BINARY...: ${BINARY}"
  echo "TAR_FILE.: ${TAR_FILE}"

  if [ ! -e "${TAR_FILE?}" ]; then
    wget https://github.com/mikefarah/yq/releases/download/v${VERSION?}/${TAR_FILE?}
  fi

  tar xvf "${TAR_FILE?}" "./${BINARY?}"

  if [ -e "${BINARY?}" ]; then
    mkdir -p "${HOME}/bin"
    mv ${BINARY} "${HOME}/bin/yq"
    rm "${TAR_FILE?}"
  fi

  ${HOME}/bin/yq --version
fi
