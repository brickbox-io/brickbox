#!/bin/bash

url=$1
instance=$2
xml_data=$3

echo "$xml_data" >> bash_errors.log

curl -X POST https://"$url"/api/vmlog/ -d "level=20&virt_brick=$instance&message=Successfully%20SSH%20connection%20to%20host,%20creating%20$instance."    # Logging

sudo virt-clone --original brickbox-U20.04 --name "$instance" --auto-clone 2>> bash_errors.log

if sudo virsh domblklist "$instance" | grep "\/var\/lib\/libvirt\/images\/$instance.img"; then


    curl -X POST https://"$url"/api/vmlog/ -d "level=20&virt_brick=$instance&message=VM%20clone%20validated."             # Logging


    curl -X POST https://dev.brickbox.io/vm/state/ -d "instance=$instance&verify=clone" &

    rm /home/bb_dev/GPU.xml 2>> bash_errors.log

    sleep 1

    echo "$xml_data" >> /home/bb_dev/GPU.xml 2>> bash_errors.log


    curl -X POST https://"$url"/api/vmlog/ -d "level=20&virt_brick=$instance&message=GPU%20XML%0D%0A$xml_data"                  # Logging


    sudo virsh attach-device "$instance" /home/bb_dev/GPU.xml 2>> bash_errors.log

    sleep 10


    if sudo virsh dumpxml "$instance" | grep "hostdev"; then

        curl -X POST https://"$url"/api/vmlog/ -d "level=20&virt_brick=$instance&message=GPU%20attached%20successfully."  # Logging

    else

        curl -X POST https://"$url"/api/vmlog/ -d "level=30&virt_brick=$instance&message=Attempting%20to%20attach%20GPU%20again."           # Logging

        sudo virsh start "$instance" 2>> bash_errors.log

        sleep 10

        sudo virsh attach-device "$instance" /home/bb_dev/GPU.xml 2>> bash_errors.log

        sleep 10

        sudo virsh reboot "$instance" 2>> bash_errors.log

    fi


    if sudo virsh dumpxml "$instance" | grep "hostdev"; then

        curl -X POST https://"$url"/api/vmlog/ -d "level=20&virt_brick=$instance&message=GPU%20attached%20successfully."  # Logging

    else

        curl -X POST https://"$url"/api/vmlog/ -d "level=40&virt_brick=$instance&message=Failled%20to%20attach%20GPU."    # Logging

    fi


    sudo virsh start "$instance" 2>> bash_errors.log

    rm /home/bb_dev/GPU.xml 2>> bash_errors.log

    curl https://dev.brickbox.io/vm/register/"$instance"/"$(sudo virsh domuuid "$instance")"/ &

    echo "VM Cloned"

else

    curl -X POST https://dev.brickbox.io/vm/error/ -d "instance=$instance&error=clone" &

fi

exit
