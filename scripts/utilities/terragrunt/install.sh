#!/bin/bash
set -e

if ! which terragrunt &> /dev/null; then
  LATEST_GITHUB_RELEASE_VERSION=$(curl -sL https://github.com/gruntwork-io/terragrunt/releases | grep -oP 'releases/tag/\K[^\"]+' | sort --version-sort | tail -1)

  echo "downloading terragrunt: ${LATEST_GITHUB_RELEASE_VERSION?}"

  wget --quiet https://github.com/gruntwork-io/terragrunt/releases/download/${LATEST_GITHUB_RELEASE_VERSION?}/terragrunt_linux_amd64

  chmod +x terragrunt_linux_amd64

  mkdir -p ${HOME?}/bin

  mv terragrunt_linux_amd64 ${HOME?}/bin/terragrunt

  terragrunt -version
fi
