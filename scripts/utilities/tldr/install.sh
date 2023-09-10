#!/bin/bash
set -e

if ! which tldr &> /dev/null; then
  if ! which npm &> /dev/null; then
    npm install -g tldr
  fi
fi
