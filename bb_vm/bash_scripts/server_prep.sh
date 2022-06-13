#!/bin/bash

# Script used to prepare the condinating server (brickbox.io) for SSH tunneling.

sudo useradd -m -s /bin/true sshtunnel
sudo mkdir -p ~sshtunnel/.ssh

sudo chown -R sshtunnel:sshtunnel ~sshtunnel/.ssh
sudo chmod 700 ~sshtunnel/.ssh

sudo touch ~sshtunnel/.ssh/authorized_keys
sudo chmod 600 ~sshtunnel/.ssh/authorized_keys
sudo chown sshtunnel ~sshtunnel/.ssh/authorized_keys

sudo chmod 600 /opt/brickbox/bb_vm/keys/bb_root
sudo chmod 644 /opt/brickbox/bb_vm/keys/bb_root.pub
