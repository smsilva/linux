#!/bin/bash
if ! which hclq &> /dev/null; then
  curl -sSLo install.sh https://install.hclq.sh

  sh install.sh
fi
