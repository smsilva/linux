#!/bin/bash
export BASE_DIR="/tmp"
export WSL_CONF_FILE="${BASE_DIR?}/wsl.conf"
export RESOLVCONF_FILE="${BASE_DIR?}/resolv.conf"
export IPS_FILE="${BASE_DIR?}/ips.txt"
export NAME_SERVERS_FILE="${BASE_DIR?}/nameservers.txt"

create_wsl_conf_file() {
  cat <<EOF | tee "${WSL_CONF_FILE?}" > /dev/null
[boot]
systemd=true

[network]
generateResolvConf = false
EOF
}

create_resolv_conf_file() {
  export FIRST_IP_ADDRESS=$(grep "^nameserver" /etc/resolv.conf \
  | head -1 \
  | awk '{ print $2 }')

  cat <<EOF | sudo tee "${RESOLVCONF_FILE?}" > /dev/null
nameserver ${FIRST_IP_ADDRESS?} # wsl default name server
EOF

  while read -r NAME_SERVER_IP; do
    echo "nameserver ${NAME_SERVER_IP?}" | sudo tee -a "${RESOLVCONF_FILE?}" > /dev/null
  done < "${IPS_FILE?}"

  cat <<EOF | sudo tee -a "${RESOLVCONF_FILE?}" > /dev/null
nameserver 8.8.8.8
nameserver 8.8.4.4

EOF

  cat "${NAME_SERVERS_FILE?}" \
  | sort \
  | while read -r SEARCH_SERVER; do
    echo "search ${SEARCH_SERVER?}" | sudo tee -a "${RESOLVCONF_FILE?}" > /dev/null
  done
}

if [ ! -f "${IPS_FILE?}" ]; then
  echo "Please create a file with the name ${IPS_FILE?} and add the IP addresses of your DNS servers."
  exit 1
fi

if [ ! -f "${NAME_SERVERS_FILE?}" ]; then
  echo "Please create a file with the name ${NAME_SERVERS_FILE?} and add the name servers."
  exit 1
fi

create_wsl_conf_file

create_resolv_conf_file

cat <<EOF

Backup of your files first:

  sudo cp /etc/resolv.conf /etc/resolv.conf.bak
  sudo cp /etc/wsl.conf /etc/wsl.conf.bak


Run the following commands:

  sudo unlink /etc/resolv.conf"
  sudo cp ${RESOLVCONF_FILE?} /etc/resolv.conf"
  sudo cp ${WSL_CONF_FILE?} /etc/wsl.conf"

EOF
