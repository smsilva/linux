#!/bin/bash
set -e

echo "Downloading..."

wget https://releases.hashicorp.com/terraform/1.0.1/terraform_1.0.1_linux_amd64.zip

unzip terraform_1.0.1_linux_amd64.zip

rm terraform_1.0.1_linux_amd64.zip

chmod +x terraform

mkdir -p ${HOME?}/bin

mv terraform ${HOME?}/bin/terraform

terraform -version
