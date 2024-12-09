#!/bin/bash
if ! which terraform > /dev/null; then
  version=$(
    curl \
      --silent \
      --url https://releases.hashicorp.com/terraform \
    | grep --perl-regexp --only-matching '(?<=/terraform/)[^/]+' \
    | sort --unique --version-sort --reverse \
    | grep --invert-match --extended-regexp "alpha|beta|rc" \
    | head -1  
  )

  file_name="terraform_${version?}_linux_amd64.zip"
  
  wget https://releases.hashicorp.com/terraform/${version?}/${file_name?}
  
  unzip ${file_name?}
  
  rm ${file_name?}
  
  chmod +x terraform
  
  mkdir -p ${HOME?}/bin
  
  mv terraform ${HOME?}/bin/terraform
fi
