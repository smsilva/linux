#!/bin/bash
if ! which ollama > /dev/null; then
  curl -fsSL https://ollama.com/install.sh | sh
fi
