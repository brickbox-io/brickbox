#!/bin/bash

url=$1
device=$2
pcie=$3

# cd /vfio-pci-bind || exit 1

command_output=$(sudo ./vfio-pci-bind/vfio-pci-bind.sh "$device" "$pcie" 2>> bash_errors.log)

# Verify that the GPU was attached sucessfully
if sudo lspci -s "$pcie" -k | grep "vfio-pci"; then

    curl -X POST https://"$url"/api/vmlog/ -d "level=20&virt_brick=NA&message=$pcie%20Driver%20set%20to%20VFIO&command_output=$command_output"  # Logging

else

    curl -X POST https://"$url"/api/vmlog/ \
    -d "level=40" \
    -d "virt_brick=NA" \
    -d "message=Failed set $pcie driver set to VFIO." \
    -d "command=sudo ./vfio-pci-bind/vfio-pci-bind.sh $device $pcie 2>> bash_errors.log"
    -d "command_output=$command_output" > /dev/null &

fi

# sudo ip link add name br0 type bridge
# sudo ip link set dev br0 up
# sudo ip link set dev enp3s0f1 master br0

# sudo dhclient -r
# sudo dhclient

exit
