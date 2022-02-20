#!/bin/bash

url=$1
instance=$2
xml_data=$3

# ---------------------------------------------------------------------------- #
#                                    Logging                                   #
# ---------------------------------------------------------------------------- #
function log {
    log_file=brick_gpu.log
    echo "$(date) - $1" >> $log_file
}

log "START - brick_gpu.sh started with url=$url, instance=$instance"

# Remote Logging
curl -X POST https://"$url"/api/vmlog/ \
-d "level=20" \
-d "virt_brick=$instance" \
-d "message=Attaching GPU to VM."

if [[ -f GPU.xml ]]; then
    sudo rm GPU.xml 2>> bash_errors.log
    log "GPU.xml was removed sucessfully." # Logging
fi

sudo echo "$xml_data" | sudo tee -a GPU.xml > /dev/null 2>> bash_errors.log

# Remote Logging
curl -X POST https://"$url"/api/vmlog/ \
-d "level=20" \
-d "virt_brick=$instance" \
-d "message=GPU XML%0D%0A$xml_data"

last_command_output=$(sudo virsh attach-device "$instance" GPU.xml --persistent 2>> bash_errors.log)
last_command=!!

sleep 20

if sudo virsh dumpxml "$instance" | grep "hostdev"; then

    log "GPU was attached sucessfully." # Logging

    # Remote Logging
    curl -X POST https://"$url"/api/vmlog/ \
    -d "level=20" \
    -d "virt_brick=$instance" \
    -d "message=GPU attached successfully."

else

    log "GPU was not attached sucessfully, attempting to attach again." # Logging

    # Remote Logging
    curl -X POST https://"$url"/api/vmlog/ \
    -d "level=30" \
    -d "virt_brick=$instance" \
    -d "message=Attempting to attach GPU again" \
    -d "command=$last_command" \
    -d "command_output=$last_command_output"

    sudo virsh start "$instance" 2>> bash_errors.log
    sudo virsh autostart "$instance" 2>> /dev/null # Enable autostart.

    sleep 20

    sudo virsh attach-device "$instance" GPU.xml --persistent 2>> bash_errors.log

    sleep 20

    sudo virsh reboot "$instance" 2>> bash_errors.log

    # Verify that the GPU was attached sucessfully the second time.
    if sudo virsh dumpxml "$instance" | grep "hostdev"; then
        log "GPU was attached sucessfully." # Logging

        # Remote Logging
        curl -X POST https://"$url"/api/vmlog/ \
        -d "level=20" \
        -d "virt_brick=$instance" \
        -d "message=GPU attached successfully."
    else
        log "GPU was not attached sucessfully." # Logging

        # Remote Logging
        curl -X POST https://"$url"/api/vmlog/ \
        -d "level=40" \
        -d "virt_brick=$instance" \
        -d "message=Failled to attach GPU."
    fi

fi

if [[ -f GPU.xml ]]; then
    sudo rm GPU.xml 2>> bash_errors.log
fi
