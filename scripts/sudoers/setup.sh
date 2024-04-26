#!/bin/bash
CURRENT_USERNAME=$1
SUDOER_FILE="/etc/sudoers.d/${CURRENT_USERNAME}"

if [[ ! -e "${SUDOER_FILE?}" ]]; then
  echo "Creating ${SUDOER_FILE?} file:"

  cat << EOF | sudo tee ${SUDOER_FILE?}
${CURRENT_USERNAME} ALL=(ALL) NOPASSWD: ALL
EOF

fi
