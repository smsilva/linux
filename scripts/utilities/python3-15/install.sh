#!/bin/bash
python_version="3.15"

if ! which "python${python_version}" &> /dev/null; then
  sudo apt-get install --yes \
    software-properties-common

  sudo add-apt-repository --yes ppa:deadsnakes/ppa

  sudo apt-get update -q

  sudo apt-get install --yes \
    "python${python_version}" \
    "python${python_version}-dev" \
    "python${python_version}-venv"

  # The system Python stays registered as the fallback; the newest wins on priority
  priority=1
  for python_binary in /usr/bin/python3.12 /usr/bin/python3.14 "/usr/bin/python${python_version}"; do
    if [[ -x "${python_binary}" ]]; then
      sudo update-alternatives \
        --install /usr/local/bin/python3 python3 "${python_binary}" "${priority}"
      priority=$((priority + 1))
    fi
  done
fi
