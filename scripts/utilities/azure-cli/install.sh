#!/bin/bash
set -e

if ! which az > /dev/null; then
  curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

  az version
fi
