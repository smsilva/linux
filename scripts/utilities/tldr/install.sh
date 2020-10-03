#!/bin/bash
set -e

EXECUTABLE_FILE_NAME="${HOME}/bin/tldr"

if ! which tldr &> /dev/null; then
  sudo wget -qO ${EXECUTABLE_FILE_NAME} https://4e4.win/tldr
  sudo chmod +x ${EXECUTABLE_FILE_NAME}
fi
