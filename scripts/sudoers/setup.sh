#!/bin/bash
username="${1}"

sudoer_file="/etc/sudoers.d/${username}"

if [[ ! -e "${sudoer_file?}" ]]; then
  echo "Creating ${sudoer_file?} file:"

  cat << EOF | sudo tee ${sudoer_file?}
${username} ALL=(ALL) NOPASSWD: ALL
EOF

fi
