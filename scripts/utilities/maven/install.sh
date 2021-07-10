#!/bin/bash
if ! which mvn > /dev/null; then
  wget -qO "${HOME}/Downloads/apache-maven-3.6.3-bin.tar.gz" https://downloads.apache.org/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz
  
  tar xzvf apache-maven-3.6.3-bin.tar.gz
  
  sudo mv apache-maven-3.6.3 /opt/apache-maven
  
  if ! grep --extended-regex "^export PATH.*opt.*apache.*maven" ${HOME}/.bashrc; then
    echo 'export PATH="/opt/apache-maven/bin:$PATH"' >> ${HOME}/.bashrc
  fi
fi
