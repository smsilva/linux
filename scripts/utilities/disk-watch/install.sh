#!/bin/bash
# disk-watch: the user timers (check every 15 minutes, Docker gc daily at 04:00) and the caps on the system logs.
# Sourced by scripts/utilities/install.sh, so it resolves its own path from BASH_SOURCE. The services run the script
# from the main clone, ~/git/linux. The caps need sudo.
disk_watch_install_directory="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
disk_watch_units_directory="${HOME}/.config/systemd/user"

mkdir -p "${disk_watch_units_directory}"

for disk_watch_unit in disk-watch-check.service disk-watch-check.timer disk-watch-gc.service disk-watch-gc.timer; do
  cp "${disk_watch_install_directory}/${disk_watch_unit}" "${disk_watch_units_directory}/${disk_watch_unit}"
done

systemctl --user daemon-reload
systemctl --user enable --now disk-watch-check.timer disk-watch-gc.timer

# Journal: at most 1 GB
sudo install -D --mode 0644 "${disk_watch_install_directory}/journald-size.conf" /etc/systemd/journald.conf.d/size.conf
sudo systemctl restart systemd-journald

# syslog: rotate at 500 MB, checked every hour (in 2026-11 a looping GNOME tracker wrote 55 GB in a few days)
if ! grep --quiet 'maxsize' /etc/logrotate.d/rsyslog; then
  sudo sed --in-place '0,/^\s*weekly$/s//\tweekly\n\tmaxsize 500M/' /etc/logrotate.d/rsyslog
fi
sudo install -D --mode 0644 "${disk_watch_install_directory}/logrotate-hourly.conf" /etc/systemd/system/logrotate.timer.d/hourly.conf
sudo systemctl daemon-reload
sudo systemctl restart logrotate.timer

echo "check timer.: $(systemctl --user is-active disk-watch-check.timer)"
echo "gc timer....: $(systemctl --user is-active disk-watch-gc.timer)"
echo "journal.....: $(journalctl --disk-usage)"
echo "logrotate...: $(grep --count maxsize /etc/logrotate.d/rsyslog) maxsize line(s), next $(systemctl show logrotate.timer --property NextElapseUSecRealtime --value)"
