#!/bin/bash
if ! which hclq &> /dev/null; then
  curl -sSLo hclq.sh https://install.hclq.sh

  sh hclq.sh
fi
