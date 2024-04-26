#!/bin/bash
POWERLINE_CONFIG_DIRECTORY=${HOME}/.config/powerline
CONFIG_FILE_NAME=${POWERLINE_CONFIG_DIRECTORY}/config.json

is_running_on_wsl2() {
  uname -r | tr '[:upper:]' '[:lower:]' | egrep "microsoft.*wsl2" &> /dev/null
  echo $?
}

if [[ ! -e "${POWERLINE_CONFIG_DIRECTORY?}" ]]; then
  # Create a Directory
  mkdir --parents "${POWERLINE_CONFIG_DIRECTORY?}"

  # Copy Powerline Config Default
  cp /usr/share/powerline/config_files/config.json ${CONFIG_FILE_NAME?}

  # Change Theme
  sed 's/default_leftonly/default/g' ${CONFIG_FILE_NAME?} --in-place

  # ~/.vimrc
  cat <<EOF > ~/.vimrc
python3 from powerline.vim import setup as powerline_setup
python3 powerline_setup()
python3 del powerline_setup
set laststatus=2
EOF

  if [[ ! $(is_running_on_wsl2) ]]; then
    # Set the VS Code Terminal Font
    VSCODE_USER_SETTINGS_FILE="${HOME}/.config/Code/User/settings.json"
    FONT_FILE_NAME="Menlo for Powerline.ttf" && \
    JQ_EXPRESSION=$(printf '."terminal.integrated.fontFamily" = "%s"' "'monospace', 'PowerlineSymbols'") && \
    echo "" && \
    echo "VSCODE_USER_SETTINGS_FILE...: ${VSCODE_USER_SETTINGS_FILE}" && \
    echo "FONT_FILE_NAME..............: ${FONT_FILE_NAME}" && \
    echo "JQ_EXPRESSION...............: ${JQ_EXPRESSION}" && \
    echo ""

    sudo wget -qO "/usr/share/fonts/${FONT_FILE_NAME}" "https://github.com/abertsch/Menlo-for-Powerline/raw/master/Menlo%20for%20Powerline.ttf"

    if [[ ! -e "${VSCODE_USER_SETTINGS_FILE}" ]]; then
      echo '{}' > "${VSCODE_USER_SETTINGS_FILE}"
      echo "$(jq "${JQ_EXPRESSION}" "${VSCODE_USER_SETTINGS_FILE}")" > "${VSCODE_USER_SETTINGS_FILE}"
    fi
  fi
fi
