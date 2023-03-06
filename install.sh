#!/bin/bash
SCRIPTS_LOCATION="${PWD}/scripts"
BIN_USER_LOCATION="${HOME}/bin-${USER##*\\}"
CURRENT_USERNAME="${USER##*\\}"

chmod +x ${SCRIPTS_LOCATION}/*

if ! [ -e ${BIN_USER_LOCATION} ]; then
  ln --symbolic ${SCRIPTS_LOCATION}/bin/ ${BIN_USER_LOCATION} &> /dev/null
fi

BASH_ALIASES_FILE="${HOME}/.bash_aliases"

if ! [ -e "${BASH_ALIASES_FILE}" ]; then
  ln --symbolic "${SCRIPTS_LOCATION}/bash_aliases" "${BASH_ALIASES_FILE}" &> /dev/null
fi

BASH_CONFIG_FILE="${HOME}/.bash_config"

if ! [ -e "${BASH_CONFIG_FILE}" ]; then
  ln --symbolic "${SCRIPTS_LOCATION}/bash_config" "${BASH_CONFIG_FILE}" &> /dev/null
fi

if ! grep --quiet --extended-regexp ".bash_config" ~/.bashrc; then
cat <<EOF >> ~/.bashrc
if [ -f ~/.bash_config ]; then
  . ~/.bash_config
fi
EOF
fi

mkdir -p ${HOME?}/bin

source ${HOME?}/.bashrc

scripts/sudoers/setup.sh "${CURRENT_USERNAME?}"
scripts/vscode/install.sh
scripts/utilities/install.sh

source ${HOME?}/.bashrc

echo "Done"
