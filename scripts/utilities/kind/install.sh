#!/bin/bash
EXECUTABLE_FILE_NAME="${HOME}/bin/kind"

if ! which kind > /dev/null; then
  curl -Lo "${EXECUTABLE_FILE_NAME}" https://kind.sigs.k8s.io/dl/v0.18.0/kind-linux-amd64

  chmod +x "${EXECUTABLE_FILE_NAME}"
fi
