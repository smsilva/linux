#!/bin/bash
curl -s https://packagecloud.io/install/repositories/datawireio/telepresence/script.deb.sh | sudo bash

sudo apt install --no-install-recommends telepresence --yes
