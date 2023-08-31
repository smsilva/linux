#!/bin/bash
set -e

if ! which helm > /dev/null; then
  VERSION="3.12.3"
  FILE_NAME="helm-v${VERSION?}-linux-amd64.tar.gz"

  wget https://get.helm.sh/${FILE_NAME?}
  
  tar xvf ${FILE_NAME?} linux-amd64/helm
  
  rm ${FILE_NAME?}
  
  chmod +x linux-amd64/helm
  
  mkdir -p ${HOME?}/bin
  
  mv linux-amd64/helm ${HOME?}/bin/helm
fi

helm version
