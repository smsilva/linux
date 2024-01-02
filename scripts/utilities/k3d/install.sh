#!/bin/bash
if ! which k3d > /dev/null; then
  wget --quiet --output-document - https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash
fi
