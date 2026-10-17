#!/bin/bash
# Piper text-to-speech with the Brazilian Portuguese voice used by scripts/bin/speak.
piper_voice="${PIPER_VOICE:-pt_BR-cadu-medium}"
piper_voice_directory="${HOME}/.local/share/piper"
piper_voice_name="${piper_voice#*-}"
piper_voice_language="${piper_voice%%-*}"
piper_voice_url="https://huggingface.co/rhasspy/piper-voices/resolve/main/${piper_voice_language%%_*}/${piper_voice_language}/${piper_voice_name%-*}/${piper_voice_name##*-}"

if ! which pw-play > /dev/null; then
  sudo apt-get install --yes -q pipewire-bin
fi

if ! which piper > /dev/null; then
  uv tool install --python 3.12 piper-tts
fi

mkdir -p "${piper_voice_directory}"

for piper_voice_file in "${piper_voice}.onnx" "${piper_voice}.onnx.json"; do
  if [[ ! -e "${piper_voice_directory}/${piper_voice_file}" ]]; then
    curl \
      --silent \
      --show-error \
      --location \
      --fail \
      --output "${piper_voice_directory}/${piper_voice_file}" \
      "${piper_voice_url}/${piper_voice_file}"
  fi
done

echo "piper..: $(which piper)"
echo "voice..: ${piper_voice_directory}/${piper_voice}.onnx"
