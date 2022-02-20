#!/bin/bash

url=$1
instance=$2


# ---------------------------------------------------------------------------- #
#                                    Logging                                   #
# ---------------------------------------------------------------------------- #
function log {
    log_file=brick_boot.log
    echo "$(date) - $1" >> $log_file
}

log "START - brick_boot.sh started with url=$url, instance=$instance"

# Check if brick is on, if not, start it.
if [ "$(sudo virsh domstate "$instance")" != "running" ]; then
    log "Brick $instance is not running, starting it."
    sudo virsh start "$instance" 2>> bash_errors.log
    sudo virsh autostart "$instance" 2>> /dev/null # Enable autostart.
    sleep 10
fi

curl https://"$url"/vm/register/"$instance"/"$(sudo virsh domuuid "$instance")"/ 2>> bash_errors.log

log "END - Successfully completed brick_img.sh" # Logging

exit 0
