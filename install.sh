#!/bin/bash
SCRIPTS_LOCATION="${PWD}/scripts"
BIN_USER_LOCATION="${HOME}/bin-${USER}"

chmod +x ${SCRIPTS_LOCATION}/*

ln --symbolic ${SCRIPTS_LOCATION}/bin/ ${BIN_USER_LOCATION} > /dev/null

BASH_ALIASES_FILE="${HOME}/.bash_aliases"

if [[ -e ${BASH_ALIASES_FILE} ]]; then
  mv ${BASH_ALIASES_FILE} ${HOME}/.bash_aliases_backup
fi

ln --symbolic ${SCRIPTS_LOCATION}/aliases.sh ${HOME}/.bash_aliases > /dev/null

FIND_EXPRESSION='(^PATH*.)(.*bin-BIN_USER$)'

if ! grep --quiet --extended-regexp "${FIND_EXPRESSION/BIN_USER/$USER}" ~/.bashrc; then
  echo "PATH=\${PATH}:${BIN_USER_LOCATION}" >> ${HOME}/.bashrc
fi

source ${HOME}/.bashrc

scripts/sudoers/install.sh
scripts/utilities/install.sh
