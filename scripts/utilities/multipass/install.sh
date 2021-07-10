#!/bin/bash
if ! which multipass > /dev/null; then
  sudo snap install multipass --classic --beta
fi
