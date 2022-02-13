#!/bin/bash

# ---------------------------------- Process --------------------------------- #
# 1) SSH into host with available hardware.
# 2) Clone template to img with virtual brick ID as name.
# 3) Validate clone as done sucsessfully.
# 4) Remove GPU.xml file left from previous attempt.
# 5) Create a file that contains the XML for the GPU that will be attached. (Or create a uniqely named XML file.)
# 6) Attach the GPU to the VM using the XML file
# 7) Verify that the GPU was attached sucessfully
# 8) Remove GPU XML file (or don't)
# 9) Boot the VM for the first time.
# 10) Report back the UUID of the new VM.
# 11) Exit

url=$1
instance=$2
xml_data=$3
root_pass=$4

# sudo echo "$xml_data" | sudo tee -a bash_errors.log > /dev/null

# ---------------------------------------------------------------------------- #
#                                    Logging                                   #
# ---------------------------------------------------------------------------- #
#script_name=$(basename -s .sh "$BASH_SOURCE[0]")

function log {
    log_file=brick_img.log
    echo "$(date) - $1" >> $log_file
}

log "START - brick_img.sh started with url=$url, instance=$instance"

# Remote Logging
curl -X POST https://"$url"/api/vmlog/ \
-d "level=20" \
-d "virt_brick=$instance" \
-d "message=Successfully SSH connection to host, creating $instance."

# ------------------------------ Clone Template ------------------------------ #

last_command_output=$(sudo virt-clone --original brickbox-U20.04 --name "$instance" --auto-clone 2>> bash_errors.log)
last_command="sudo virt-clone --original brickbox-U20.04 --name $instance --auto-clone"
sudo virt-customize -a /var/lib/libvirt/images/"$instance".img --root-password password:"$root_pass" 2>> bash_errors.log

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


    curl -X POST https://"$url"/vm/state/ -d "instance=$instance&verify=clone" &

    if [[ -f GPU.xml ]]; then
        sudo rm GPU.xml 2>> bash_errors.log
        log "GPU.xml was removed sucessfully." # Logging
    fi

    sleep 1

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



    sudo virsh start "$instance" 2>> bash_errors.log
    sudo virsh autostart "$instance" 2>> /dev/null # Enable autostart.

    if [[ -f GPU.xml ]]; then
        sudo rm GPU.xml 2>> bash_errors.log
    fi

    curl https://"$url"/vm/register/"$instance"/"$(sudo virsh domuuid "$instance")"/ 2>> bash_errors.log

    log "END - Successfully completed brick_img.sh" # Logging

    exit 0

else

    log "END - $instance.img failed to clone." # Logging

    # Remote Logging
    curl -X POST https://"$url"/vm/error/ \
    -d "instance=$instance" \
    -d "error=clone" 2>> bash_errors.log

    exit 1

fi
