#!/bin/bash

# url=$1
device=$2
pcie=$3

# cd /vfio-pci-bind || exit 1

sudo ./vfio-pci-bind/vfio-pci-bind.sh "$device" "$pcie" 2>> bash_errors.log

sudo ip link add name br0 type bridge
sudo ip link set dev br0 up
sudo ip link set dev enp3s0f1 master br0

sudo dhclient -r
sudo dhclient

exit
