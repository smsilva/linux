#!/bin/bash
# Tailscale: WireGuard-based private network. Run "sudo tailscale up --operator=${USER}" afterwards to log in.
if ! which tailscale > /dev/null; then
  curl \
    --fail \
    --silent \
    --show-error \
    --location \
    https://tailscale.com/install.sh | sh
fi

echo "tailscale..: $(which tailscale)"
echo "version....: $(tailscale version | head -1)"
