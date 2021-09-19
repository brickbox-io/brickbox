#!/bin/bash

# --------------------------------- Arguments -------------------------------- #
# - (1) Instance ID that has been provided to refrence this new VM.
# - (2) XML formatted data to attach GPU to VM

# ---------------------------------- Process --------------------------------- #
# 1) Clone template to img with virtual brick ID as name.
# 2) Validate clone as done sucsessfully.
# 3) Remove GPU.xml file left from previous attempt.


instance=$1
xml_data=$2

sshpass -p "Password@1" ssh -p 9002 bb_dev@localhost << EOF
sleep 1

sudo virt-clone --original brickbox-U20.04 --name $instance --auto-clone &&

if sudo virsh domblklist $instance | grep "\/var\/lib\/libvirt\/images\/$instance.img"; then

    curl -X POST https://dev.brickbox.io/vm/state/ -d "instance=$instance&verify=clone" &

    rm /home/bb_dev/GPU.xml 2>> bash_errors.log
    echo "$xml_data" >> GPU.xml 2>> bash_errors.log

    sudo virsh attach-device $instance /home/bb_dev/GPU.xml && 2>> bash_errors.log

    sudo virsh start $instance &&

    rm /home/bb_dev/GPU.xml 2>> bash_errors.log

    curl https://dev.brickbox.io/vm/register/$instance/\$(sudo virsh domuuid $instance)/ &

    echo "VM Cloned"

else

    curl -X POST https://dev.brickbox.io/vm/error/ -d "instance=$instance&error=clone" &

fi

exit

EOF
