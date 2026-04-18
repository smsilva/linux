#!/bin/bash
font_dir="${HOME}/.local/share/fonts/HackNerdFont"
terminator_config="${HOME}/.config/terminator/config"

if [[ ! -d "${font_dir}" ]]; then
  echo "Downloading Hack Nerd Font..."

  tmp_zip=$(mktemp --suffix=.zip)

  wget --quiet --show-progress \
    --output-document="${tmp_zip}" \
    "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/Hack.zip"

  mkdir --parents "${font_dir}"
  unzip -q "${tmp_zip}" -d "${font_dir}"
  rm "${tmp_zip}"

  fc-cache --force "${font_dir}"

  echo "Hack Nerd Font installed at ${font_dir}"
fi

if [[ ! -f "${terminator_config}" ]]; then
  mkdir --parents "$(dirname "${terminator_config}")"

  cat <<EOF > "${terminator_config}"
[global_config]
[keybindings]
[profiles]
  [[default]]
    font = Hack Nerd Font 12
    use_system_font = False
[layouts]
  [[default]]
    [[[window0]]]
      type = Window
      parent = ""
    [[[child1]]]
      type = Terminal
      parent = window0
[plugins]
EOF

  echo "Terminator configured to use Hack Nerd Font"
else
  if ! grep --quiet "use_system_font" "${terminator_config}"; then
    sed --in-place '/\[\[default\]\]/a\    font = Hack Nerd Font 12\n    use_system_font = False' "${terminator_config}"
    echo "Terminator font updated in existing config"
  else
    sed --in-place \
      --expression 's/use_system_font = True/use_system_font = False/' \
      --expression 's/font = .*/font = Hack Nerd Font 12/' \
      "${terminator_config}"
    echo "Terminator font updated"
  fi
fi
