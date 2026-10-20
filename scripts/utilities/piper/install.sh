#!/bin/bash
# Piper text-to-speech with the Brazilian Portuguese voice used by scripts/bin/speak.
# Sourced by scripts/utilities/install.sh, so it resolves its own path from BASH_SOURCE.
piper_install_directory="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
piper_voice="${PIPER_VOICE:-pt_BR-cadu-medium}"

export PATH="${HOME}/.local/bin:${PATH}"

if ! which pw-play > /dev/null; then
  sudo apt-get install --yes -q pipewire-bin
fi

if ! which uv > /dev/null; then
  curl --silent --show-error --location --fail https://astral.sh/uv/install.sh | sh
fi

if ! which piper > /dev/null; then
  uv tool install --python 3.12 piper-tts
fi

"${piper_install_directory}/../../bin/piper-voice-download" "${piper_voice}"

echo "piper..: $(which piper)"
