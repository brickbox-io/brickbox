#!/bin/bash

# Starts a brick up that is shutdown.

url=$1
instance=$2

# Check if brick is on, if not, start it.
if [ "$(sudo virsh domstate "$instance")" != "running" ]; then
    echo "Brick is not running, starting it."
    sudo virsh start "$instance"
    sleep 10
fi

# Check if brick has started.
if [ $(sudo virsh list --all | grep "$instance" | wc -l) -eq 1 ]; then
    echo "Brick started."
    curl -X POST https://"$url"/api/vmlog/ -d "level=20&virt_brick=$instance&message=Brick%20has%20started." &
    exit 0
else
    echo "Brick failed to start."
    curl -X POST https://"$url"/api/vmlog/ -d "level=40&virt_brick=$instance&message=Brick%20failed%20to%20start." &
    exit 1
fi

exit
