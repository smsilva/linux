#!/bin/bash
if ! which psql > /dev/null; then
  LOCAL_KEYRING_GPG_FILE="/usr/share/keyrings/postgresql-archive-keyring.gpg"

  wget \
    --quiet \
    --output-document - https://www.postgresql.org/media/keys/ACCC4CF8.asc \
  | gpg --dearmor \
  | sudo tee "${LOCAL_KEYRING_GPG_FILE?}"

  source /etc/os-release
  
  cat <<EOF | sudo tee /etc/apt/sources.list.d/pgdg.list
deb [signed-by=${LOCAL_KEYRING_GPG_FILE}] https://apt.postgresql.org/pub/repos/apt ${VERSION_CODENAME}-pgdg main
EOF
 
  sudo apt-get update -q

  sudo apt-get install \
    postgresql-client-15 \
    --yes \
    -q
fi
