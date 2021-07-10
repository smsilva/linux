#!/bin/bash
set -e

if ! which az > /dev/null; then
  echo "Install"
  curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
else
  echo "Already installed"
  az version
fi
