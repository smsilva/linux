#!/bin/bash
if ! which openstack > /dev/null; then
  sudo add-apt-repository cloud-archive:wallaby
  sudo apt-get install python3-openstackclient -qq
fi
