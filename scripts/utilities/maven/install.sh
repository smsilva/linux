#!/bin/bash
if ! which mvn > /dev/null; then
  MAVEN_VERSION="3.9.1"
  LOCAL_INSTALL_DIRECTORY="${HOME}/bin/apache-maven" && mkdir -p "${LOCAL_INSTALL_DIRECTORY}"
  LOCAL_DIRECTORY="${HOME}/.install/maven" && mkdir -p "${LOCAL_DIRECTORY}"
  LOCAL_ZIP_FILE="${LOCAL_DIRECTORY}/apache-maven-${MAVEN_VERSION}-bin.tar.gz"

  echo "MAVEN_VERSION............: ${MAVEN_VERSION}"
  echo "LOCAL_DIRECTORY..........: ${LOCAL_DIRECTORY}"
  echo "LOCAL_ZIP_FILE...........: ${LOCAL_ZIP_FILE}"
  echo "LOCAL_INSTALL_DIRECTORY..: ${LOCAL_INSTALL_DIRECTORY}"
  echo ""

  if [ ! -e "${LOCAL_ZIP_FILE}" ]; then
    wget -O "${LOCAL_ZIP_FILE?}" https://downloads.apache.org/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz
  fi

  tar xzf "${LOCAL_ZIP_FILE?}" --directory="${LOCAL_DIRECTORY}"

  rm -rf "${LOCAL_INSTALL_DIRECTORY?}" > /dev/null
  
  mv "${LOCAL_DIRECTORY}/apache-maven-${MAVEN_VERSION}" "${LOCAL_INSTALL_DIRECTORY}"
  
  if ! grep --quiet --extended-regex "^export PATH.*apache-maven" ${HOME}/.bashrc; then
    echo "export PATH=\"${LOCAL_INSTALL_DIRECTORY}/bin:\${PATH}\"" >> ${HOME}/.bashrc
  fi
fi
