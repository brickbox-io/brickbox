#!/bin/bash

# This script pauses the brick by shutting it down.

url=$1
instance=$2

# Check if brick has stopped.
if [ "$(sudo virsh domstate "$instance")" == "running" ]; then
    echo "Brick is still running. Shutting it down manually."
    sudo virsh shutdown  "$instance"
    sudo virsh autostart "$instance" --disable > /dev/null # Disable autostart.
    sleep 10
fi

# Confirm that brick has stopped.
if [ "$(sudo virsh domstate "$instance")" == "running" ]; then
    curl -X POST https://"$url"/api/vmlog/ -d "level=40&virt_brick=$instance&message=Could%20not%20shutdown%20instance." &
    exit 1
else
    echo "Brick has been shut down."
    curl -X POST https://"$url"/api/vmlog/ -d "level=20&virt_brick=$instance&message=Brick%20has%20been%20shutdown." &
    exit 0
fi

exit
