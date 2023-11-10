#!/bin/bash
if ! which psql > /dev/null; then
  wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc \
  | gpg --dearmor \
  | sudo tee /usr/share/keyrings/postgresql-archive-keyring.gpg
  
  echo "deb [signed-by=/usr/share/keyrings/postgresql-archive-keyring.gpg] https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" \
  | sudo tee /etc/apt/sources.list.d/pgdg.list
  
  sudo apt-get update

  sudo apt-get install \
    postgresql-client-15 \
    --yes
fi
