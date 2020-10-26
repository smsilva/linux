#!/bin/bash
set -e

if ! which trivy &> /dev/null; then
  sudo apt-get install --yes \
    wget \
    apt-transport-https \
    gnupg \
    lsb-release

  wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -

  echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee /etc/apt/sources.list.d/trivy.list

  sudo apt-get update -q

  sudo apt-get install trivy --yes -q
fi
