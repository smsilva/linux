#!/bin/bash
if ! which tfswitch > /dev/null; then
  curl -L https://raw.githubusercontent.com/warrensbox/terraform-switcher/release/install.sh | sudo bash
fi

tfswitch --version
