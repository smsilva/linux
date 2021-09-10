#!/bin/bash
set -e

LOCAL_INSTALL_FILE="/tmp/install.sh"

if ! which tgswitch > /dev/null; then
  wget -qO ${LOCAL_INSTALL_FILE?} https://raw.githubusercontent.com/warrensbox/tgswitch/release/install.sh

  bash ${LOCAL_INSTALL_FILE?} -b ${HOME?}/bin
  
  tgswitch --version
fi
