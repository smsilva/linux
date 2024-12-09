#!/bin/bash
base_dir="/tmp"
wsl_conf_file="${base_dir?}/wsl.conf"
resolvconf_file="${base_dir?}/resolv.conf"
ips_file="${base_dir?}/ips.txt"
name_servers_file="${base_dir?}/nameservers.txt"

create_wsl_conf_file() {
  cat <<EOF | tee "${wsl_conf_file?}" > /dev/null
[boot]
systemd=true

[network]
generateResolvConf = false
EOF
}

create_resolv_conf_file() {
  first_ip_address=$(grep "^nameserver" /etc/resolv.conf \
  | head -1 \
  | awk '{ print $2 }')

  cat <<EOF | sudo tee "${resolvconf_file?}" > /dev/null
nameserver ${first_ip_address?} # wsl default name server
EOF

  while read -r name_server_ip; do
    echo "nameserver ${name_server_ip?}" | sudo tee -a "${resolvconf_file?}" > /dev/null
  done < "${ips_file?}"

  cat <<EOF | sudo tee -a "${resolvconf_file?}" > /dev/null
nameserver 8.8.8.8
nameserver 8.8.4.4

EOF

  cat "${name_servers_file?}" \
  | sort \
  | while read -r SEARCH_SERVER; do
    echo "search ${SEARCH_SERVER?}" | sudo tee -a "${resolvconf_file?}" > /dev/null
  done
}

if [ ! -f "${ips_file?}" ]; then
  echo "Please create a file with the name ${ips_file?} and add the IP addresses of your DNS servers."
  exit 1
fi

if [ ! -f "${name_servers_file?}" ]; then
  echo "Please create a file with the name ${name_servers_file?} and add the name servers."
  exit 1
fi

create_wsl_conf_file

create_resolv_conf_file

cat <<EOF

Backup your files first:

  sudo cp /etc/resolv.conf /etc/resolv.conf.bak
  sudo cp /etc/wsl.conf /etc/wsl.conf.bak


Run the following commands:

  sudo unlink /etc/resolv.conf
  sudo cp ${resolvconf_file?} /etc/resolv.conf
  sudo cp ${wsl_conf_file?} /etc/wsl.conf

EOF
