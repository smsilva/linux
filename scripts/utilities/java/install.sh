#!/bin/bash
if ! which java &> /dev/null; then
  sudo apt-get install openjdk-11-jre-headless -q --yes
fi
