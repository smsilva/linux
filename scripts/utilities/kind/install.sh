#!/bin/bash
if ! which kind > /dev/null; then
  executable_file_name="${HOME}/bin/kind"
  github_owner="kubernetes-sigs"
  github_repository="kind"

  latest_release=$(
    curl \
      --silent "https://api.github.com/repos/${github_owner?}/${github_repository?}/releases/latest" \
      | grep '"tag_name"' \
      | sed -E 's|(.*")([^"]+)(".*)|\2|'
  )

  curl \
    --location \
    --url https://kind.sigs.k8s.io/dl/${latest_release?}/kind-linux-amd64 \
    --output "${executable_file_name?}"

  chmod +x "${executable_file_name?}"
fi
