#!/bin/bash
set -e

node_major_fallback=24

nodejs_latest_lts_major() {
  curl --fail --silent --location https://nodejs.org/dist/index.json \
  | tr '{' '\n' \
  | grep '"lts":"' \
  | head --lines 1 \
  | grep --only-matching --perl-regexp '(?<="version":"v)\d+'
}

nodejs_current_major() {
  if ! command -v node > /dev/null; then
    return 0
  fi

  node --version | grep --only-matching --perl-regexp '(?<=^v)\d+'
}

nodejs_install() {
  local node_major="${1?}"

  sudo apt-get update --quiet

  sudo apt-get install --yes \
    ca-certificates \
    curl \
    gnupg

  sudo mkdir -p /etc/apt/keyrings

  curl --fail --silent --show-error --location https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key \
  | sudo gpg \
    --yes \
    --dearmor \
    --output /etc/apt/keyrings/nodesource.gpg

  cat <<EOF | sudo tee /etc/apt/sources.list.d/nodesource.list
deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${node_major}.x nodistro main
EOF

  sudo apt-get update --quiet

  sudo apt-get install --yes --quiet nodejs
}

npm_configure() {
  if ! command -v npm > /dev/null; then
    return 0
  fi

  mkdir -p "${HOME}/.npm-packages"

  npm config set prefix "${HOME}/.npm-packages"

  if ! command -v tldr > /dev/null; then
    npm install --global tldr
  fi
}

main() {
  local node_major
  local current_major

  node_major="$(nodejs_latest_lts_major || true)"
  node_major="${node_major:-${node_major_fallback}}"

  current_major="$(nodejs_current_major)"

  if [ "${current_major}" = "${node_major}" ]; then
    echo "Node.js já está na última major LTS (v${current_major})"
  else
    echo "Instalando Node.js ${node_major}.x (atual: ${current_major:-nenhum})"

    nodejs_install "${node_major}"
  fi

  node --version

  npm_configure
}

main "$@"
