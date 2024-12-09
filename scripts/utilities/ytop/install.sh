#!/bin/bash
if ! which ytop > /dev/null; then
  set -e

  version=$(curl \
    --silent "https://api.github.com/repos/cjbassi/ytop/releases/latest" \
    | grep '"tag_name"' \
    | awk -F '"' '{ print $4 }'
  )

  install_dir="${HOME}/bin/"

  tar_file="ytop-${version?}-x86_64-unknown-linux-gnu.tar.gz"
  
  wget "https://github.com/cjbassi/ytop/releases/download/${version}/${tar_file}"
  
  [ ! -e "${install_dir}" ] && mkdir "${install_dir}"
  
  tar xvf "${tar_file}" && \
  mv ytop "${install_dir}" && \
  rm "${tar_file}"
  
  mkdir -p ${HOME}/.config/ytop/
  
  cp scripts/utilities/ytop/monokai.json ~/.config/ytop/monokai.json
fi
