#!/bin/bash
if [[ ! -e "/usr/share/icons/Paper" ]]; then
  sudo apt-get install paper-icon-theme --yes -q
fi
