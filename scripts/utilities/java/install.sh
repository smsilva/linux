#!/bin/bash
if ! which java > /dev/null; then
  sudo apt-get install openjdk-17-jre-headless -q --yes
fi
