#!/bin/bash
SCRIPTS_LOCATION="${PWD}/scripts"
BIN_USER_LOCATION="${HOME}/bin-${USER}"

chmod +x ${SCRIPTS_LOCATION}/*

ln --symbolic ${SCRIPTS_LOCATION}/bin/ ${BIN_USER_LOCATION} > /dev/null

BASH_ALIASES_FILE="${HOME}/.bash_aliases"

if [[ -e ${BASH_ALIASES_FILE} ]]; then
  mv ${BASH_ALIASES_FILE} ${HOME}/.bash_aliases_backup
fi

ln --symbolic ${SCRIPTS_LOCATION}/aliases.sh ${HOME}/.bash_aliases

echo "PATH=\${PATH}:${BIN_USER_LOCATION}" >> ${HOME}/.bashrc

source ${HOME}/.bashrc
