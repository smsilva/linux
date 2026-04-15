#!/bin/bash

if ! which helm > /dev/null; then
  target_dir="${HOME}/bin"

  mkdir --parents "${target_dir}"

  latest_version=$(
    curl \
      --silent \
      --fail \
      "https://api.github.com/repos/helm/helm/releases/latest" \
    | grep '"tag_name"' \
    | sed --regexp-extended 's|.*"([^"]+)".*|\1|'
  )

  if [[ -z "${latest_version}" ]]; then
    echo "Failed to retrieve the latest version of helm" >&2
    exit 1
  fi

  remote_file="helm-${latest_version}-linux-amd64.tar.gz"

  file_url="https://get.helm.sh/${remote_file?}"

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
      --strip-components 1 \
      linux-amd64/helm

  chmod +x "${target_dir}/helm"
fi

helm version
