#!/bin/bash
set -e

if ! grep --quiet --extended-regexp "today-fortune" ~/.bashrc; then
cat <<EOF >> ~/.bashrc

today-fortune
EOF
fi
