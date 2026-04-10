#!/bin/bash

# Install istioctl — Istio CLI
# https://istio.io/latest/docs/setup/getting-started/#download

if ! which istioctl > /dev/null; then
  target_dir="${HOME}/bin"
  mkdir -p "${target_dir}"

  latest_version=$(
    curl \
      --silent \
      --fail \
      "https://api.github.com/repos/istio/istio/releases/latest" \
    | grep '"tag_name"' \
    | sed -E 's|.*"([^"]+)".*|\1|'
  )

  curl \
    --fail \
    --silent \
    --show-error \
    --location \
    "https://github.com/istio/istio/releases/download/${latest_version?}/istioctl-${latest_version}-linux-amd64.tar.gz" \
  | tar \
    --extract \
    --gzip \
    --file - \
    --directory "${target_dir}" \
    istioctl

  chmod +x "${target_dir}/istioctl"
fi

istioctl version --remote=false
