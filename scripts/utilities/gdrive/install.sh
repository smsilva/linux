#!/bin/bash
# Google Drive folder mounted with rclone + fuse3 (systemd user service), used as the bridge with the voice conversation.
# Sourced by scripts/utilities/install.sh, so it resolves its own path from BASH_SOURCE.
gdrive_install_directory="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

"${gdrive_install_directory}/../../bin/gdrive-mount"
