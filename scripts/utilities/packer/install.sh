#!/bin/bash
set -e

if ! which packer > /dev/null; then

  curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
  
  sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
  
  sudo apt-get update -qq && \
  sudo apt-get install packer -qq
fi
