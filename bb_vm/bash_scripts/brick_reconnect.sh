#!/bin/bash

url=$1
device=$2
pcie=$3

cd /vfio-pci-bind
sudo ./vfio-pci-bind.sh "$device" "$pcie"

exit
