#!/bin/bash
# Ubuntu's apt repository lags behind upstream, so install the .deb from the latest GitHub release.

flameshot_install() {
  local release_json
  local latest_version
  local installed_version
  local ubuntu_version
  local architecture
  local zip_url
  local work_dir
  local deb_file

  release_json=$(
    curl \
      --silent \
      --fail \
      "https://api.github.com/repos/flameshot-org/flameshot/releases/latest"
  )

  latest_version=$(
    echo "${release_json}" \
    | grep '"tag_name"' \
    | sed --regexp-extended 's|.*"v?([^"]+)".*|\1|'
  )

  if [[ -z "${latest_version}" ]]; then
    echo "Failed to retrieve the latest version of flameshot" >&2
    return 1
  fi

  installed_version=$(dpkg-query --show --showformat='${Version}' flameshot 2>/dev/null)

  if [[ "${installed_version%%-*}" == "${latest_version}" ]]; then
    echo "flameshot ${latest_version} already installed"
    return 0
  fi

  ubuntu_version=$(. /etc/os-release && echo "${VERSION_ID}")
  architecture=$(dpkg --print-architecture)

  zip_url=$(
    echo "${release_json}" \
    | grep '"browser_download_url"' \
    | grep "artifact-ubuntu-${ubuntu_version}-${architecture}.zip\"" \
    | sed --regexp-extended 's|.*"(https://[^"]+)".*|\1|'
  )

  if [[ -z "${zip_url}" ]]; then
    echo "No flameshot ${latest_version} package for ubuntu-${ubuntu_version}-${architecture}" >&2
    return 1
  fi

  echo "version..: ${latest_version}"
  echo "installed: ${installed_version:-none}"
  echo "package..: ${zip_url}"

  work_dir=$(mktemp --directory)

  (
    cd "${work_dir}" \
    && curl \
      --fail \
      --silent \
      --show-error \
      --location \
      --output package.zip \
      "${zip_url}" \
    && curl \
      --fail \
      --silent \
      --show-error \
      --location \
      --output package.zip.sha256sum \
      "${zip_url}.sha256sum" \
    && [[ "$(cut --delimiter ' ' --fields 1 package.zip.sha256sum)" == "$(sha256sum package.zip | cut --delimiter ' ' --fields 1)" ]] \
    && unzip -q package.zip \
    && sha256sum --check --quiet ./*.deb.sha256sum
  ) || {
    echo "Failed to download or verify the flameshot package" >&2
    rm --recursive --force "${work_dir}"
    return 1
  }

  deb_file=$(ls "${work_dir}"/*.deb)

  sudo apt-get install --yes -q "${deb_file}"

  rm --recursive --force "${work_dir}"
}

# GNOME keeps Print for its own screenshot UI, so bind flameshot to Super+Shift+S instead.
flameshot_keybinding() {
  local schema="org.gnome.settings-daemon.plugins.media-keys"
  local path="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/flameshot/"
  local current

  if ! which gsettings > /dev/null; then
    return 0
  fi

  current=$(gsettings get "${schema}" custom-keybindings)

  if [[ "${current}" != *"'${path}'"* ]]; then
    if [[ "${current}" == "@as []" || "${current}" == "[]" ]]; then
      gsettings set "${schema}" custom-keybindings "['${path}']"
    else
      gsettings set "${schema}" custom-keybindings "${current%]}, '${path}']"
    fi
  fi

  gsettings set "${schema}.custom-keybinding:${path}" name "Flameshot"
  gsettings set "${schema}.custom-keybinding:${path}" command "flameshot gui"
  gsettings set "${schema}.custom-keybinding:${path}" binding "<Super><Shift>s"

  echo "keybinding: Super+Shift+S -> flameshot gui"
}

flameshot_install

flameshot_keybinding

flameshot --version
