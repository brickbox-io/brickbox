#!/bin/bash

url=$1
instance=$2

# ---------------------------------------------------------------------------- #
#                                    Logging                                   #
# ---------------------------------------------------------------------------- #
function log {
    log_file=brick_clone.log
    echo "$(date) - $1" >> $log_file
}

log "START - brick_clone.sh started with url=$url, instance=$instance"

# Remote Logging
curl -X POST https://"$url"/api/vmlog/ \
-d "level=20" \
-d "virt_brick=$instance" \
-d "message=Attempting to create base image."

# ------------------------------ Clone Template ------------------------------ #

last_command_output=$(sudo virt-clone --original brickbox-U20.04 --name "$instance" --auto-clone 2>> bash_errors.log)
last_command="sudo virt-clone --original brickbox-U20.04 --name $instance --auto-clone"

if sudo virsh domblklist "$instance" | grep "\/var\/lib\/libvirt\/images\/$instance.img"; then

    log "$instance.img was cloned sucessfully." # Logging

    # Remote Logging
    curl -X POST https://"$url"/api/vmlog/ \
    -d "level=20" \
    -d "host=1" \
    -d "virt_brick=$instance" \
    -d "message=VM clone validated" \
    -d "command=$last_command" \
    -d "command_output=$last_command_output"

    # Update Brick Status
    curl -X POST https://"$url"/vm/state/ -d "instance=$instance&verify=clone"

    exit 0

else

    log "END - $instance.img failed to clone." # Logging

    # Remote Error Handling
    curl -X POST https://"$url"/vm/error/ \
    -d "instance=$instance" \
    -d "error=clone" 2>> bash_errors.log

    exit 1

fi
