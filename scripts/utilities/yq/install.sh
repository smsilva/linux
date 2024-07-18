#!/bin/bash
if ! which yq > /dev/null; then
  BINARY="yq_linux_amd64"
  TAR_FILE="${BINARY?}.tar.gz"
  VERSION=$(curl \
    --silent "https://api.github.com/repos/mikefarah/yq/releases/latest" \
    | grep '"tag_name"' \
    | sed -E 's|(.*")([^"]+)(".*)|\2|'
  )

  echo "VERSION..: ${VERSION}"
  echo "BINARY...: ${BINARY}"
  echo "TAR_FILE.: ${TAR_FILE}"

  if [[ ! -e "${TAR_FILE?}" ]]; then
    wget https://github.com/mikefarah/yq/releases/download/${VERSION?}/${TAR_FILE?}
  fi

  tar xvf "${TAR_FILE?}" "./${BINARY?}"

  if [[ -e "${BINARY?}" ]]; then
    mkdir -p "${HOME}/bin"
    mv ${BINARY} "${HOME}/bin/yq"
    rm "${TAR_FILE?}"
  fi

  ${HOME}/bin/yq --version
fi
