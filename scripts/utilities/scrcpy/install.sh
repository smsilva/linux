#!/bin/bash
# scrcpy: mirror an Android screen over USB (alias "scr" in scripts/bash_aliases).
# The apt package is too old for recent Android versions, so install the GitHub release.
scrcpy_target_dir="${HOME}/.local/opt/scrcpy"
scrcpy_binary="${HOME}/.local/bin/scrcpy"

if [[ ! -x "${scrcpy_binary}" ]]; then
  scrcpy_version=$(
    curl \
      --silent \
      --fail \
      "https://api.github.com/repos/Genymobile/scrcpy/releases/latest" \
    | grep '"tag_name"' \
    | sed --regexp-extended 's|.*"([^"]+)".*|\1|'
  )

  if [[ -z "${scrcpy_version}" ]]; then
    echo "Failed to retrieve the latest version of scrcpy" >&2
  else
    scrcpy_tar_file="scrcpy-linux-x86_64-${scrcpy_version}.tar.gz"
    scrcpy_release_url="https://github.com/Genymobile/scrcpy/releases/download/${scrcpy_version}"
    scrcpy_download_dir="$(mktemp --directory)"

    if curl \
        --fail \
        --silent \
        --show-error \
        --location \
        --output "${scrcpy_download_dir}/${scrcpy_tar_file}" \
        "${scrcpy_release_url}/${scrcpy_tar_file}" \
      && curl \
        --fail \
        --silent \
        --show-error \
        --location \
        --output "${scrcpy_download_dir}/SHA256SUMS.txt" \
        "${scrcpy_release_url}/SHA256SUMS.txt" \
      && (cd "${scrcpy_download_dir}" && grep " ${scrcpy_tar_file}$" SHA256SUMS.txt | sha256sum --check --status); then
      rm --recursive --force "${scrcpy_target_dir}"
      mkdir --parents "${scrcpy_target_dir}" "${HOME}/.local/bin"

      tar \
        --extract \
        --gzip \
        --file "${scrcpy_download_dir}/${scrcpy_tar_file}" \
        --directory "${scrcpy_target_dir}" \
        --strip-components 1

      ln --symbolic --force "${scrcpy_target_dir}/scrcpy" "${scrcpy_binary}"
    else
      echo "Failed to download or verify ${scrcpy_tar_file}" >&2
    fi

    rm --recursive --force "${scrcpy_download_dir}"
  fi
fi

echo "scrcpy..: ${scrcpy_binary}"
echo "version.: $("${scrcpy_binary}" --version 2>/dev/null | head -1)"
