#!/bin/bash
if ! which yq > /dev/null; then
  sudo snap install yq
fi
