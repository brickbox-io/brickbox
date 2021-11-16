#!/bin/bash

# Starts a brick up that is shutdown.

url=$1
instance=$2

# Check if brick is on, if not, start it.
if [ "$(sudo virsh domstate "$instance")" != "running" ]; then
    echo "Brick is not running, starting it."
    command_output=$(sudo virsh start "$instance")
    sleep 10
fi

# Check if brick has started.
# if [ "$(sudo virsh list --all | grep -c "$instance")" -eq 1 ]; then
    if [ "$(sudo virsh domstate "$instance")" != "running" ]; then
    echo "Brick started."

    curl -s -X POST https://"$url"/api/vmlog/ \
    -d "level=20" \
    -d "virt_brick=$instance" \
    -d "message=Brick hasstarted." \
    -d "command=sudo virsh start $instance" \
    -d "command_output=$command_output" > /dev/null &

    exit 0
else
    echo "Brick failed to start."
    curl -X POST https://"$url"/api/vmlog/ -d "level=40&virt_brick=$instance&message=Brick%20failed%20to%20start." &
    exit 1
fi

exit
