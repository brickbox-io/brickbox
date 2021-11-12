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

sudo echo "$xml_data" | sudo tee -a bash_errors.log > /dev/null

# Logging
curl -X POST https://"$url"/api/vmlog/ -d "level=20&virt_brick=$instance&message=Successfully%20SSH%20connection%20to%20host,%20creating%20$instance."

# ------------------------------ Clone Template ------------------------------ #

last_command_output=$(sudo virt-clone --original brickbox-U20.04 --name "$instance" --auto-clone 2>> bash_errors.log)
last_command="sudo virt-clone --original brickbox-U20.04 --name $instance --auto-clone"

if sudo virsh domblklist "$instance" | grep "\/var\/lib\/libvirt\/images\/$instance.img"; then

    # Logging
    curl -X POST https://"$url"/api/vmlog/ -d "level=20&host=1&virt_brick=$instance&message=VM%20clone%20validated&command=$last_command&command_output=$last_command_output"


    curl -X POST https://dev.brickbox.io/vm/state/ -d "instance=$instance&verify=clone" &

    sudo rm GPU.xml 2>> bash_errors.log

    sleep 1

    sudo echo "$xml_data" | sudo tee -a GPU.xml > /dev/null 2>> bash_errors.log


    # Logging
    curl -X POST https://"$url"/api/vmlog/ -d "level=20&virt_brick=$instance&message=GPU%20XML%0D%0A$xml_data"


    last_command_output=$(sudo virsh attach-device "$instance" GPU.xml --persistent 2>> bash_errors.log)
    last_command=!!

    sleep 20


    if sudo virsh dumpxml "$instance" | grep "hostdev"; then

        curl -X POST https://"$url"/api/vmlog/ -d "level=20&virt_brick=$instance&message=GPU%20attached%20successfully."  # Logging

    else

        # Logging
        curl -X POST https://"$url"/api/vmlog/ -d "level=30&virt_brick=$instance&message=Attempting%20to%20attach%20GPU%20again&command=$last_command&command_output=$last_command_output"

        sudo virsh start "$instance" 2>> bash_errors.log

        sleep 20

        sudo virsh attach-device "$instance" GPU.xml --persistent 2>> bash_errors.log

        sleep 20

        sudo virsh reboot "$instance" 2>> bash_errors.log

    fi

    # Verify that the GPU was attached sucessfully
    if sudo virsh dumpxml "$instance" | grep "hostdev"; then

        curl -X POST https://"$url"/api/vmlog/ -d "level=20&virt_brick=$instance&message=GPU%20attached%20successfully."  # Logging

    else

        curl -X POST https://"$url"/api/vmlog/ -d "level=40&virt_brick=$instance&message=Failled%20to%20attach%20GPU."    # Logging

    fi


    {
        sudo virsh start "$instance"
    }   2>> bash_errors.log

    sudo rm GPU.xml 2>> bash_errors.log

    curl https://dev.brickbox.io/vm/register/"$instance"/"$(sudo virsh domuuid "$instance")"/ 2>> bash_errors.log

    echo "VM Cloned"

else

    curl -X POST https://dev.brickbox.io/vm/error/ -d "instance=$instance&error=clone" 2>> bash_errors.log

fi

exit
