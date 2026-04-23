#!/bin/bash
if ! which python3.14 &> /dev/null; then
  sudo apt-get install --yes \
    software-properties-common

  sudo add-apt-repository --yes ppa:deadsnakes/ppa

  sudo apt-get update -q

  sudo apt-get install --yes \
    python3.14 \
    python3.14-dev \
    python3.14-venv

  sudo update-alternatives \
    --install /usr/local/bin/python3 python3 /usr/bin/python3.12 1

  sudo update-alternatives \
    --install /usr/local/bin/python3 python3 /usr/bin/python3.14 2
fi
