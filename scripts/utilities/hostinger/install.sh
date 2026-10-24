#!/bin/bash
# Hostinger API CLI (https://github.com/hostinger/api-cli). Run "hostinger auth login" afterwards to sign in.
if ! which hostinger > /dev/null; then
  target_dir="${HOME}/bin"

  mkdir --parents "${target_dir}"

  latest_version=$(
    curl \
      --silent \
      --fail \
      "https://api.github.com/repos/hostinger/api-cli/releases/latest" \
    | grep '"tag_name"' \
    | sed --regexp-extended 's|.*"v([^"]+)".*|\1|'
  )

  if [[ -z "${latest_version}" ]]; then
    echo "Failed to retrieve the latest version of the Hostinger CLI" >&2
    exit 1
  fi

  remote_file="hostinger-${latest_version?}-linux-amd64.tar.gz"

  checksums_file="hostinger-${latest_version?}-checksums.sha256"

  base_url="https://github.com/hostinger/api-cli/releases/download/v${latest_version?}"

  download_dir=$(mktemp --directory)

  curl \
    --fail \
    --silent \
    --show-error \
    --location \
    --output "${download_dir}/${remote_file}" \
    "${base_url}/${remote_file}"

  curl \
    --fail \
    --silent \
    --show-error \
    --location \
    --output "${download_dir}/${checksums_file}" \
    "${base_url}/${checksums_file}"

  if ! (cd "${download_dir}" && sha256sum --check --ignore-missing --quiet "${checksums_file}"); then
    echo "Checksum verification failed for ${remote_file}" >&2
    rm --recursive --force "${download_dir}"
    exit 1
  fi

  tar \
    --extract \
    --gzip \
    --file "${download_dir}/${remote_file}" \
    --directory "${target_dir}" \
    hostinger

  chmod +x "${target_dir}/hostinger"

  rm --recursive --force "${download_dir}"
fi

echo "hostinger..: $(which hostinger)"
echo "version....: $(hostinger version | head -1)"
