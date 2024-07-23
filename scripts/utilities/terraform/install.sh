#!/bin/bash
if ! which terraform > /dev/null; then
  VERSION=$(
    curl \
      --silent \
      --url https://releases.hashicorp.com/terraform \
    | grep --perl-regexp --only-matching '(?<=/terraform/)[^/]+' \
    | sort --unique --version-sort --reverse \
    | grep --invert-match --extended-regexp "alpha|beta|rc" \
    | head -1  
  )

  FILE_NAME="terraform_${VERSION?}_linux_amd64.zip"
  
  wget https://releases.hashicorp.com/terraform/${VERSION?}/${FILE_NAME?}
  
  unzip ${FILE_NAME?}
  
  rm ${FILE_NAME?}
  
  chmod +x terraform
  
  mkdir -p ${HOME?}/bin
  
  mv terraform ${HOME?}/bin/terraform
fi
