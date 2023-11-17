#!/bin/bash
export BASE_DIR="/tmp"
export WSL_CONF_FILE="${BASE_DIR?}/wsl.conf"
export RESOLVCONF_FILE="${BASE_DIR?}/resolv.conf"
export IPS_FILE="${BASE_DIR?}/ips.txt"
export NAME_SERVERS_FILE="${BASE_DIR?}/nameservers.txt"

override_wsl_conf() {
  cat <<EOF | tee "${WSL_CONF_FILE?}" > /dev/null
[boot]
systemd=true

[network]
generateResolvConf = false
EOF
}

generate_resolv_conf_file() {
  export FIRT_IP_ADDRESS=$(grep "^nameserver" /etc/resolv.conf \
  | head -1 \
  | awk '{ print $2 }')

  cat <<EOF | sudo tee "${RESOLVCONF_FILE?}" > /dev/null
nameserver ${FIRT_IP_ADDRESS?} # wsl default name server
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

override_wsl_conf

generate_resolv_conf_file

echo ""
echo "Run the following command to copy the ${RESOLVCONF_FILE?} file to /etc/resolv.conf"
echo ""
echo "  sudo unlink /etc/resolv.conf"
echo "  sudo cp ${RESOLVCONF_FILE?} /etc/resolv.conf"
echo ""
echo ""

echo "Run the following command to copy the ${WSL_CONF_FILE?} file to /etc/wsl.conf"
echo ""
echo "  sudo cp ${WSL_CONF_FILE?} /etc/wsl.conf"
echo ""
