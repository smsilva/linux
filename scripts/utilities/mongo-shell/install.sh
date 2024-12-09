#!/bin/bash
mongosh_version="2.0.2"

if ! which mongosh > /dev/null; then
  mkdir --parents /tmp/mongo-shell/install

  wget "https://downloads.mongodb.com/compass/mongodb-mongosh_${mongosh_version?}_amd64.deb" \
    --output-document /tmp/mongo-shell/install/mongodb-mongosh.deb
  
  sudo dpkg -i /tmp/mongo-shell/install/mongodb-mongosh.deb

  rm -rf /tmp/mongo-shell/install/
fi

mongosh --version
