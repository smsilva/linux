#!/bin/bash
sudo add-apt-repository ppa:snwh/ppa --yes

# update repository info
sudo apt-get update -qq

# install icon theme
sudo apt-get install paper-icon-theme -qq
