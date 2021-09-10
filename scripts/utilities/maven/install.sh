#!/bin/bash
if ! which mvn > /dev/null; then
  MAVEN_VERSION="3.6.3"
  LOCAL_INSTALL_DIRECTORY="${HOME}/bin/apache-maven" && mkdir -p "${LOCAL_INSTALL_DIRECTORY}"
  LOCAL_DIRECTORY="${HOME}/.install/maven" && mkdir -p "${LOCAL_DIRECTORY}"
  LOCAL_ZIP_FILE="${LOCAL_DIRECTORY}/apache-maven-${MAVEN_VERSION}-bin.tar.gz"

  wget -qO "${LOCAL_ZIP_FILE?}" https://downloads.apache.org/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz
  
  tar xzvf "${LOCAL_ZIP_FILE?}" --directory="${LOCAL_DIRECTORY}"
  
  sudo mv "${LOCAL_DIRECTORY}/apache-maven-3.6.3" "${LOCAL_INSTALL_DIRECTORY}"
  
  if ! grep --extended-regex "^export PATH.*apache.*maven" ${HOME}/.bashrc; then
    echo "export PATH=\"${LOCAL_INSTALL_DIRECTORY}/bin:\${PATH}\"" >> ${HOME}/.bashrc
  fi
fi
