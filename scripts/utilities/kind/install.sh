#!/bin/bash
if ! which kind > /dev/null; then
  EXECUTABLE_FILE_NAME="${HOME}/bin/kind"
  GITHUB_OWNER="kubernetes-sigs"
  GITHUB_REPOSITORY="kind"

  LATEST_RELEASE=$(
    curl \
      --silent "https://api.github.com/repos/${GITHUB_OWNER?}/${GITHUB_REPOSITORY?}/releases/latest" \
      | grep '"tag_name"' \
      | sed -E 's|(.*")([^"]+)(".*)|\2|'
  )

  curl \
    --location \
    --url https://kind.sigs.k8s.io/dl/${LATEST_RELEASE?}/kind-linux-amd64 \
    --output "${EXECUTABLE_FILE_NAME?}"

  chmod +x "${EXECUTABLE_FILE_NAME?}"
fi
