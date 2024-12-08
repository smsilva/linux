#!/bin/bash
logon_screen_background_image_file="${HOME}/Pictures/logon-screen.jpg"
background_change_local_command="${HOME}/bin/change-gdm-background"
background_change_remote_command="https://raw.githubusercontent.com/thiggy01/change-gdm-background/master/change-gdm-background"

if [ -e ${logon_screen_background_image_file?} ]; then
  cp /usr/share/backgrounds/matt-mcnulty-nyc-2nd-ave.jpg ${logon_screen_background_image_file?}

  sudo apt install \
    libglib2.0-dev-bin -y -qq

  wget --output-document ${background_change_local_command?} ${background_change_remote_command?}

  chmod +x ${background_change_local_command?}

  echo "y" | sudo ${background_change_local_command?} ${logon_screen_background_image_file?}
fi
