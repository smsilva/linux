#!/bin/bash

if ! which k9s > /dev/null; then
  target_dir="${HOME}/bin"

  mkdir --parents "${target_dir}"

  latest_version=$(
    curl \
      --silent \
      --fail \
      "https://api.github.com/repos/derailed/k9s/releases/latest" \
    | grep '"tag_name"' \
    | sed --regexp-extended 's|.*"([^"]+)".*|\1|'
  )

  if [[ -z "${latest_version}" ]]; then
    echo "Failed to retrieve the latest version of k9s" >&2
    exit 1
  fi

  remote_file="k9s_Linux_amd64.tar.gz"
  
  file_url="https://github.com/derailed/k9s/releases/download/${latest_version?}/${remote_file?}"

  curl \
    --fail \
    --silent \
    --show-error \
    --location \
    "${file_url?}" \
  | tar \
      --extract \
      --gzip \
      --file - \
      --directory "${target_dir}" \
      k9s

  chmod +x "${target_dir}/k9s"
fi

k9s version
