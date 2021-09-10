#!/bin/bash
set -e

if ! which tfswitch > /dev/null; then
  curl -L https://raw.githubusercontent.com/warrensbox/terraform-switcher/release/install.sh | sudo bash

  tfswitch --version
fi
