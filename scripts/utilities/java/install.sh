#!/bin/bash
if ! which java > /dev/null; then
  sudo apt-get install openjdk-17-jdk-headless -q --yes
fi
