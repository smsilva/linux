#!/bin/bash
set -e

if ! which terraform > /dev/null; then
  VERSION="1.0.2"
  FILE_NAME="terraform_${VERSION?}_linux_amd64.zip"
  
  wget https://releases.hashicorp.com/terraform/${VERSION?}/${FILE_NAME?}
  
  unzip ${FILE_NAME?}
  
  rm ${FILE_NAME?}
  
  chmod +x terraform
  
  mkdir -p ${HOME?}/bin
  
  mv terraform ${HOME?}/bin/terraform
fi

terraform -version
