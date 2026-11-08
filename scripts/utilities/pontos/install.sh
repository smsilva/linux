#!/bin/bash
# Pontos: the systemd user timer of the daily classification check (pontos-classification-check, 05:30 local).
# Sourced by scripts/utilities/install.sh, so it resolves its own path from BASH_SOURCE. The service runs the script
# from the main clone, ~/git/linux.
pontos_install_directory="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
pontos_units_directory="${HOME}/.config/systemd/user"

mkdir -p "${pontos_units_directory}"

for pontos_unit in pontos-classification-check.service pontos-classification-check.timer; do
  cp "${pontos_install_directory}/${pontos_unit}" "${pontos_units_directory}/${pontos_unit}"
done

systemctl --user daemon-reload
systemctl --user enable --now pontos-classification-check.timer

echo "timer.......: $(systemctl --user is-active pontos-classification-check.timer)"
echo "next run....: $(systemctl --user show pontos-classification-check.timer --property NextElapseUSecRealtime --value)"
