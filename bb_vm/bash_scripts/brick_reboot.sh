#!/bin/bash

url=$1
instance=$2

# Reboot the brick
sudo virsh reboot "$instance"

# Confirm the brick is running, exit after 30 seconds
for i in {1..30}; do
    if sudo virsh list --all | grep -q "$instance"; then
        echo "Brick $instance is running"
        curl -X POST https://"$url"/api/vmlog/ -d "level=20&virt_brick=$instance&message=Brick%20has%20rebooted." &
        exit 0
    fi
    echo "$i"
    sleep 1
done

# Check if the brick is not running
if ! sudo virsh list --all | grep -q "$instance"; then
    echo "Brick $instance is not running"
    curl -X POST https://"$url"/api/vmlog/ -d "level=40&virt_brick=$instance&message=Brick%20has%20failed%20to%20reboot." &
    exit 1
fi

exit
