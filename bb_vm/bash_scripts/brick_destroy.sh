#!/bin/bash

# Need to change folder permissions
# sudo chown -R bb_dev boot/

url=$1
instance=$2

sleep 1

sudo virsh shutdown  "$instance"

sudo virsh destroy "$instance"

sudo virsh undefine "$instance"

sleep 5

# sudo -n rm /var/lib/libvirt/images/"$instance".qcow2 2>> bash_errors.log

sudo rm /var/lib/libvirt/images/"$instance".img 2>> bash_errors.log

# Confirm that the image is deleted
if [ -f /var/lib/libvirt/images/"$instance".img ]; then

    curl -X POST https://"$url"/api/vmlog/ \
    -d "level=50" \
    -d "virt_brick=$instance"\
    -d "message=Brick was not destroyed."

    exit 1
fi

# files=$(sudo ls /var/lib/libvirt/images/)

# curl -X POST https://"$url"/vm/host/garbage \
# -d "files=$files"

exit 0
