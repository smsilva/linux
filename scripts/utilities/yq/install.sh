#!/bin/bash
if ! which yq > /dev/null; then
  binary="yq_linux_amd64"
  tar_file="${binary?}.tar.gz"
  version=$(curl \
    --silent "https://api.github.com/repos/mikefarah/yq/releases/latest" \
    | grep '"tag_name"' \
    | awk -F '"' '{ print $4 }'
  )

  echo "version..: ${version}"
  echo "binary...: ${binary}"
  echo "tar_file.: ${tar_file}"

  if [[ ! -e "${tar_file?}" ]]; then
    wget https://github.com/mikefarah/yq/releases/download/${version?}/${tar_file?}
  fi

  tar xvf "${tar_file?}" "./${binary?}"

  if [[ -e "${binary?}" ]]; then
    mkdir -p "${HOME}/bin"
    mv ${binary} "${HOME}/bin/yq"
    rm "${tar_file?}"
  fi

  ${HOME}/bin/yq --version
fi
