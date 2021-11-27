#!/bin/bash
SCRIPTS_LOCATION="${PWD}/scripts"
BIN_USER_LOCATION="${HOME}/bin-${USER}"

chmod +x ${SCRIPTS_LOCATION}/*

if ! [ -e ${BIN_USER_LOCATION} ]; then
  ln --symbolic ${SCRIPTS_LOCATION}/bin/ ${BIN_USER_LOCATION} &> /dev/null
fi

BASH_ALIASES_FILE="${HOME}/.bash_aliases"

if ! [ -e "${BASH_ALIASES_FILE}" ]; then
  ln --symbolic "${SCRIPTS_LOCATION}/aliases.sh" "${BASH_ALIASES_FILE}" &> /dev/null
fi

BASH_CONFIG_FILE="${HOME}/.bash_config"

if ! [ -e "${BASH_CONFIG_FILE}" ]; then
  ln --symbolic "${SCRIPTS_LOCATION}/bash_config" "${BASH_CONFIG_FILE}" &> /dev/null
fi

FIND_EXPRESSION='(^PATH*.)(.*bin-BIN_USER$)'

if ! grep --quiet --extended-regexp "${FIND_EXPRESSION/BIN_USER/$USER}" ~/.bashrc; then
  echo "PATH=\${PATH}:${BIN_USER_LOCATION}" >> ${HOME}/.bashrc
fi

mkdir -p ${HOME?}/bin

source ${HOME?}/.bashrc

scripts/sudoers/setup.sh
scripts/vscode/install.sh
scripts/utilities/install.sh

source ~/.bashrc

echo "Done"
