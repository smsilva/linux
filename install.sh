#!/bin/bash
scripts_location="${PWD}/scripts"
user_scripts_location="${HOME}/.scripts"
current_username="${USER##*\\}"

bash_aliases_file="${HOME}/.bash_aliases"
bash_config_file="${HOME}/.bash_config"
bash_functions_file="${HOME}/.bash_functions"

git_global_templates="${HOME}/.git-templates"
claude_global_md_file="${HOME}/.claude/CLAUDE.md"
claude_settings_file="${HOME}/.claude/settings.json"
claude_statusline_file="${HOME}/.claude/statusline.sh"

chmod +x ${scripts_location}/*

if [[ ! -e "${user_scripts_location}" ]]; then
  ln --symbolic "${scripts_location}/bin/" "${user_scripts_location}" &> /dev/null
fi

if [[ ! -e "${git_global_templates}" ]]; then
  ln --symbolic "${scripts_location}/git" "${git_global_templates}"

  git config --global init.templatedir "${git_global_templates}"
fi

if [[ ! -e "${claude_global_md_file}" ]]; then
  ln --symbolic "${PWD}/claude/CLAUDE.md" "${claude_global_md_file}" &> /dev/null
fi

if [[ ! -e "${claude_settings_file}" ]]; then
  ln --symbolic "${PWD}/claude/settings.json" "${claude_settings_file}" &> /dev/null
fi

if [[ ! -e "${claude_statusline_file}" ]]; then
  ln --symbolic "${PWD}/scripts/bin/claude-status-line" "${claude_statusline_file}" &> /dev/null
fi

if [[ ! -e "${bash_aliases_file}" ]]; then
  ln --symbolic "${scripts_location}/bash_aliases" "${bash_aliases_file}" &> /dev/null
fi

if [[ ! -e "${bash_config_file}" ]]; then
  ln --symbolic "${scripts_location}/bash_config" "${bash_config_file}" &> /dev/null
fi

if [[ ! -e "${bash_functions_file}" ]]; then
  ln --symbolic "${scripts_location}/bash_functions" "${bash_functions_file}" &> /dev/null
fi

if ! grep --quiet --extended-regexp ".bash_config" "${HOME}/.bashrc"; then
  cat <<EOF >> ~/.bashrc

if [[ -f ~/.bash_config ]]; then
  . ~/.bash_config
fi
EOF
fi

# US International keyboard to work with cedilla
if ! grep --quiet --extended-regexp "GTK_IM_MODULE=cedilla" /etc/environment; then
  echo "export GTK_IM_MODULE=cedilla" | sudo tee --append /etc/environment
fi

if ! grep --quiet --extended-regexp "QT_IM_MODULE=cedilla" /etc/environment; then
  echo "export QT_IM_MODULE=cedilla" | sudo tee --append /etc/environment
fi

if [[ ! -f "${HOME}/.XCompose" ]]; then
  cat <<EOF > "${HOME}/.XCompose"
# UTF-8 (Unicode) compose sequences

# Overrides C acute with Ccedilla:
<dead_acute> <C> : "Ç" "Ccedilla"
<dead_acute> <c> : "ç" "ccedilla"
EOF
fi

mkdir --parents ${HOME}/bin

source ${HOME}/.bashrc

scripts/sudoers/setup.sh "${current_username?}"
scripts/vscode/install.sh
scripts/utilities/install.sh

source ${HOME}/.bashrc

echo "Done"
