#!/bin/bash
scripts_location="${PWD}/scripts"
bin_user_location="${HOME}/bin-${USER##*\\}"
current_username="${USER##*\\}"
git_global_templates="${HOME}/.git-templates"

chmod +x ${scripts_location}/*

if ! [ -e "${bin_user_location}" ]; then
  ln --symbolic "${scripts_location}/bin/" "${bin_user_location}" &> /dev/null
fi

if ! [ -e "${git_global_templates}" ]; then
  ln --symbolic "${scripts_location}/git" "${git_global_templates}"

  git config --global init.templatedir "${git_global_templates}"
fi

bash_aliases_file="${HOME}/.bash_aliases"

if ! [ -e "${bash_aliases_file}" ]; then
  ln --symbolic "${scripts_location}/bash_aliases" "${bash_aliases_file}" &> /dev/null
fi

bash_config_file="${HOME}/.bash_config"

if ! [ -e "${bash_config_file}" ]; then
  ln --symbolic "${scripts_location}/bash_config" "${bash_config_file}" &> /dev/null
fi

if ! grep --quiet --extended-regexp ".bash_config" ~/.bashrc; then
  cat <<EOF >> ~/.bashrc
if [ -f ~/.bash_config ]; then
  . ~/.bash_config
fi
EOF
fi

# US International keyboard to work with cedilla
if ! grep --quiet --extended-regexp "GTK_IM_MODULE=cedilla" /etc/environment; then
  echo "export GTK_IM_MODULE=cedilla" | sudo tee --append /etc/environment
fi

mkdir -p ${HOME?}/bin

source ${HOME?}/.bashrc

scripts/sudoers/setup.sh "${current_username?}"
scripts/vscode/install.sh
scripts/utilities/install.sh

source ${HOME?}/.bashrc

echo "Done"
