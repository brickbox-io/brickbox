#!/bin/bash

# --------------------------------- Arguments -------------------------------- #
# - (1) Instance ID that has been provided to refrence this new VM.
# - (2) XML formatted data to attach GPU to VM

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

    sleep 1

    sudo virsh start $instance &&

    rm /home/bb_dev/GPU.xml 2>> bash_errors.log

    curl https://dev.brickbox.io/vm/register/$instance/\$(sudo virsh domuuid $instance)/ &

    echo "VM Cloned"

else

    curl -X POST https://dev.brickbox.io/vm/error/ -d "instance=$instance&error=clone" &

fi

exit

EOF
