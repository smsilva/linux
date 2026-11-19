#!/bin/bash
python_version="3.15"
# The python3 the machine runs: 3.15 stays installed beside it, but google-re2 (cel-python) has no wheel for 3.15 yet,
# so uv projects that need it fail to build on it (Nereus, 2026-11-19)
python_default="3.14"

if ! which "python${python_version}" &> /dev/null; then
  sudo apt-get install --yes \
    software-properties-common

  sudo add-apt-repository --yes ppa:deadsnakes/ppa

  sudo apt-get update -q

  sudo apt-get install --yes \
    "python${python_version}" \
    "python${python_version}-dev" \
    "python${python_version}-venv"

  # The system Python stays registered as the fallback; the newest wins on priority, unless python_default is set below
  priority=1
  for python_binary in /usr/bin/python3.12 /usr/bin/python3.14 "/usr/bin/python${python_version}"; do
    if [[ -x "${python_binary}" ]]; then
      sudo update-alternatives \
        --install /usr/local/bin/python3 python3 "${python_binary}" "${priority}"
      priority=$((priority + 1))
    fi
  done
fi

# Manual mode: the priorities above would pick the newest, and an apt upgrade would not move it back
if [[ -x "/usr/bin/python${python_default}" ]]; then
  sudo update-alternatives \
    --set python3 "/usr/bin/python${python_default}"
fi
