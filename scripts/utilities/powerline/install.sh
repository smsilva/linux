#!/bin/bash
powerline_config_directory=${HOME}/.config/powerline
config_file_name=${powerline_config_directory}/config.json

is_running_on_wsl2() {
  uname -r | tr '[:upper:]' '[:lower:]' | grep --extended-regexp "microsoft.*wsl2" &> /dev/null
  echo $?
}

if [[ ! -e "${powerline_config_directory?}" ]]; then
  # Create a Directory
  mkdir --parents "${powerline_config_directory?}"

  # Copy Powerline Config Default
  cp /usr/share/powerline/config_files/config.json ${config_file_name?}

  # Change Theme
  sed 's/default_leftonly/default/g' ${config_file_name?} --in-place

  # ~/.vimrc
  cat <<EOF > ~/.vimrc
python3 from powerline.vim import setup as powerline_setup
python3 powerline_setup()
python3 del powerline_setup
set laststatus=2
EOF

  if [[ ! $(is_running_on_wsl2) ]]; then
    # Set the VS Code Terminal Font
    vscode_user_settings_file="${HOME}/.config/Code/User/settings.json"
    font_file_name="Menlo for Powerline.ttf" && \
    jq_expression=$(printf '."terminal.integrated.fontFamily" = "%s"' "'monospace', 'PowerlineSymbols'") && \
    echo "" && \
    echo "vscode_user_settings_file...: ${vscode_user_settings_file}" && \
    echo "font_file_name..............: ${font_file_name}" && \
    echo "jq_expression...............: ${jq_expression}" && \
    echo ""

    sudo wget -qO "/usr/share/fonts/${font_file_name}" "https://github.com/abertsch/Menlo-for-Powerline/raw/master/Menlo%20for%20Powerline.ttf"

    if [[ ! -e "${vscode_user_settings_file}" ]]; then
      echo '{}' > "${vscode_user_settings_file}"
      echo "$(jq "${jq_expression}" "${vscode_user_settings_file}")" > "${vscode_user_settings_file}"
    fi
  fi
fi
