#!/bin/bash
LOGON_SCREEN_BACKGROUND_IMAGE_FILE="${HOME}/Pictures/logon-screen.jpg"
BACKGROUND_CHANGE_LOCAL_COMMAND="${HOME}/bin/change-gdm-background"
BACKGROUND_CHANGE_REMOTE_COMMAND="https://raw.githubusercontent.com/thiggy01/change-gdm-background/master/change-gdm-background"

if [ -e ${LOGON_SCREEN_BACKGROUND_IMAGE_FILE?} ]; then
  cp /usr/share/backgrounds/matt-mcnulty-nyc-2nd-ave.jpg ${LOGON_SCREEN_BACKGROUND_IMAGE_FILE?}

  sudo apt install \
    libglib2.0-dev-bin -y -qq

  wget --output-document ${BACKGROUND_CHANGE_LOCAL_COMMAND?} ${BACKGROUND_CHANGE_REMOTE_COMMAND?}

  chmod +x ${BACKGROUND_CHANGE_LOCAL_COMMAND?}

  echo "y" | sudo ${BACKGROUND_CHANGE_LOCAL_COMMAND?} ${LOGON_SCREEN_BACKGROUND_IMAGE_FILE?}
fi
