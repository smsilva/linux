#!/bin/bash
# Google Drive folder mounted with rclone + fuse3 (systemd user service), used as the bridge with the voice conversation.
# Sourced by scripts/utilities/install.sh, so it resolves its own path from BASH_SOURCE.
gdrive_install_directory="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

"${gdrive_install_directory}/../../bin/gdrive-mount"

# Request watcher: written but not enabled; enable it with "systemctl --user enable --now gdrive-request-watch.service"
gdrive_watch_service_file="${HOME}/.config/systemd/user/gdrive-request-watch.service"

cat <<EOF > "${gdrive_watch_service_file}"
[Unit]
Description=Watch the Google Drive bridge request file and notify the tmux session
After=rclone-dump-mental-prompts.service
Wants=rclone-dump-mental-prompts.service

[Service]
ExecStart=%h/.scripts/gdrive-request-watch
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload

echo "watcher.: gdrive-request-watch.service ($(systemctl --user is-enabled gdrive-request-watch.service))"
