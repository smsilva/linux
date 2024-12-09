#!/bin/bash
if ! which psql > /dev/null; then
  local_keyring_gpg_file="/usr/share/keyrings/postgresql-archive-keyring.gpg"

  wget \
    --quiet \
    --output-document - https://www.postgresql.org/media/keys/ACCC4CF8.asc \
  | gpg --dearmor \
  | sudo tee "${local_keyring_gpg_file?}"

  source /etc/os-release
  
  cat <<EOF | sudo tee /etc/apt/sources.list.d/pgdg.list
deb [signed-by=${local_keyring_gpg_file}] https://apt.postgresql.org/pub/repos/apt ${VERSION_CODENAME?}-pgdg main
EOF
 
  sudo apt-get update -q

  sudo apt-get install \
    postgresql-client-15 \
    --yes \
    -q
fi
