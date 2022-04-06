#!/bin/bash

# Script will be pre-loaded on the VM images and set to run on startup.
#
# ----------------------------- Script Functions ----------------------------- #
# 1) Ping brickbox.io with UUID, expect a return that contains an assigned port number.
# 2) Create "sshtunnel" user with key pair, provide public key to brickbox.io to be authorized.
# 3) Establish a persistant reverse SSH connection with brickbox.io using the port number provided, must allow gatway ports.
# 4) Report a ready status to brickbo.io
#
#
# -------------------------------- End Points -------------------------------- #
# /vm/tunnel/
# POST 'domain_uuid' & 'pub_key'
# Returns the port number that as been assigned to the virtual machine. Note: Post the public key for the sshtunnel account.
#
#
# ------------------------------- Pre-Configure ------------------------------ #
# Create bbvm.service file in /etc/systemd/system and enable for startup and 'chmod +x' to set executable. Finally -> systemctl enable bbvm.service
#
#####
# [Unit]
# Description=grab releveant information and establish tunnel
# [Service]
# ExecStart=/usr/local/sbin/vm_init.sh
# [Install]
# WantedBy=multi-user.target
#####

# ---------------------------------------------------------------------------- #
#                               Script Functions                               #
# ---------------------------------------------------------------------------- #

ip link set dev enp1s0 up
dhclient

# Check Existing Connection
has_connection=$(systemctl is-active --quiet sshtunnel && echo true)
if [[ $has_connection ]]; then
        exit 1
fi

# mode="DEV"

# if [ $mode == "DEV" ]; then
#         url='dev.brickbox.io'
#         ip='134.209.214.111'
# elif [ $mode == "PROD" ]; then
#         url='brickbox.io'
#         ip='143.244.165.205'
# else
#         echo "URL not set."
#         exit 1
# fi

domain_uuid=$(sudo dmidecode -s system-uuid) # VM's UUI

# SSH key Pair
sudo mkdir -p /etc/sshtunnel
sudo ssh-keygen -qN "" -f /etc/sshtunnel/id_rsa
pub_key=$(cat /etc/sshtunnel/id_rsa.pub)

# POST to server and receive assigned port for tunnel
url='dev.brickbox.io'
response=$(curl -H "Content-Type: application/x-www-form-urlencoded; charset=utf-8" \
                --data-urlencode "pub_key=$pub_key" \
                -d "domain_uuid=$domain_uuid" \
                -w "%{http_code}" \
                -X POST "https://$url/vm/tunnel/")

http_code=$(tail -c 4 <<< "$response")

if [[ $http_code != 200  ]] ; then
    url='brickbox.io'
    response=$(curl -H "Content-Type: application/x-www-form-urlencoded; charset=utf-8" \
                --data-urlencode "pub_key=$pub_key" \
                -d "domain_uuid=$domain_uuid" \
                -w "%{http_code}" \
                -X POST "https://$url/vm/tunnel/")

    http_code=$(tail -c 4 <<< "$response")

fi

if [[ $http_code != 200  ]] ; then
    echo "Failed to obtain port number."
    exit 1
fi

assigned_port=${response::-3}

# -------------------------- SSH Reverse Connection -------------------------- #
cat <<EOF > /etc/systemd/system/sshtunnel.service
[Unit]
Description = Service to maintain an ssh reverse tunnel
Wants = network-online.target
After = network-online.target
StartLimitIntervalSec = 0

[Service]
Type = simple
ExecStart = /usr/bin/ssh -qNn \\
            -o ServerAliveInterval=30 \\
            -o ServerAliveCountMax=3 \\
            -o ExitOnForwardFailure=yes \\
            -o StrictHostKeyChecking=no \\
            -o UserKnownHostsFile=/dev/null \\
            -i /etc/sshtunnel/id_rsa \\
            -R :$assigned_port:localhost:22 \\
            sshtunnel@$url -p 22

Restart = always
RestartSec = 60

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable --now sshtunnel
sudo systemctl daemon-reload

# ---------------------------- START - SSH Config ---------------------------- #
sudo sed -i '/PermitRootLogin prohibit-password/s/^#//g' /etc/ssh/sshd_config   # Tested
sed -i '/^PermitRootLogin/s/prohibit-password/yes/' /etc/ssh/sshd_config        # Tested
# sed -i '/^PermitRootLogin/s/no/yes/' /etc/ssh/sshd_config # Tested (The Default is "prohibit-password")

sudo sed -i "/^[^#]*PasswordAuthentication[[:space:]]no/c\PasswordAuthentication yes" /etc/ssh/sshd_config

sed -i '/^PasswordAuthentication/s/no/yes/' /etc/ssh/sshd_config                # Tested

sudo sed -i '/AuthorizedKeysFile/s/^#//g' /etc/ssh/sshd_config
sudo sed -i '/PubkeyAuthentication/s/^#//g' /etc/ssh/sshd_config

service ssh reload
# ----------------------------- END - SSH Config ----------------------------- #
