#!/bin/bash
EXECUTABLE_FILE_NAME="${HOME}/kind"

curl -Lo "${EXECUTABLE_FILE_NAME}" https://kind.sigs.k8s.io/dl/v0.8.1/kind-linux-amd64

chmod +x "${EXECUTABLE_FILE_NAME}"

sudo install ${EXECUTABLE_FILE_NAME} /usr/local/bin/
