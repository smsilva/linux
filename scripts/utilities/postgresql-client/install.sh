#!/bin/bash
if ! which psql > /dev/null; then
  wget --quiet --output-document - https://www.postgresql.org/media/keys/ACCC4CF8.asc \
  | gpg --dearmor \
  | sudo tee /usr/share/keyrings/postgresql-archive-keyring.gpg

  INSTALLED_DISTRIBUTION=$(lsb_release --codename --short 2> /dev/null)
  
  cat <<EOF | sudo tee /etc/apt/sources.list.d/pgdg.list
deb [signed-by=/usr/share/keyrings/postgresql-archive-keyring.gpg] https://apt.postgresql.org/pub/repos/apt $(lsb_release --codename --short)-pgdg main
EOF
 
  sudo apt-get update -q

  sudo apt-get install \
    postgresql-client-15 \
    --yes \
    -q
fi
