#!/bin/bash
# nereus-registry-cleanup: the daily user timer that runs Nereus's scripts/registry/cleanup --apply.
# Sourced by scripts/utilities/install.sh, so it resolves its own path from BASH_SOURCE. The service runs the script from
# Nereus's main clone, ~/git/getnereus/nereus; without it, nothing is installed.
nereus_registry_cleanup_directory="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
nereus_registry_cleanup_units_directory="${HOME}/.config/systemd/user"

if [[ ! -x "${HOME}/git/getnereus/nereus/scripts/registry/cleanup" ]]; then
  echo "nereus-registry-cleanup: no ~/git/getnereus/nereus/scripts/registry/cleanup, skipped"
else
  mkdir -p "${nereus_registry_cleanup_units_directory}"
  for nereus_registry_cleanup_unit in nereus-registry-cleanup.service nereus-registry-cleanup.timer; do
    cp "${nereus_registry_cleanup_directory}/${nereus_registry_cleanup_unit}" \
      "${nereus_registry_cleanup_units_directory}/${nereus_registry_cleanup_unit}"
  done
  systemctl --user daemon-reload
  systemctl --user enable --now nereus-registry-cleanup.timer
  echo "cleanup timer: $(systemctl --user is-active nereus-registry-cleanup.timer)"
fi
