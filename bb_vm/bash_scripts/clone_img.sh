#!/bin/bash

# --------------------------------- Arguments -------------------------------- #
# - (1) URL Endpint
# - (2) Instance ID that has been provided to refrence this new VM.
# - (3) XML formatted data to attach GPU to VM

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

echo "$xml_data"

if lsof -i tcp:9002; then

    sshpass -p "Password@1" ssh -p 9002 bb_dev@localhost 'bash -s' < /opt/brickbox/bb_vm/bash_scripts/temp.sh "$url" "$instance" \""$xml_data"\" 2>> /opt/brickbox/bb_vm/bash_scripts/bash_errors.log

else

    curl -X POST https://"$url"/api/vmlog/ -d "level=50&virt_brick=$instance&message=Could%20not%20connect%20to%20host%20port." &

fi

# EOF

# curl -X POST https://$url/api/vmlog/ -d "level=20&virt_brick=$instance&message=Successfully%20SSH%20connection%20to%20host,%20creating%20$instance."    # Logging

# sudo virt-clone --original brickbox-U20.04 --name $instance --auto-clone && 2>> bash_errors.log

# if sudo virsh domblklist $instance | grep "\/var\/lib\/libvirt\/images\/$instance.img"; then


#     curl -X POST https://$url/api/vmlog/ -d "level=20&virt_brick=$instance&message=VM%20clone%20validated."             # Logging


#     curl -X POST https://dev.brickbox.io/vm/state/ -d "instance=$instance&verify=clone" &

#     rm /home/bb_dev/GPU.xml && 2>> bash_errors.log

#     sleep 1

#     echo "$xml_data" >> /home/bb_dev/GPU.xml && 2>> bash_errors.log


#     curl -X POST https://$url/api/vmlog/ -d "level=20&virt_brick=$instance&message=GPU%20XML%0D%0A$xml_data"                  # Logging


#     sudo virsh attach-device $instance /home/bb_dev/GPU.xml && 2>> bash_errors.log

#     sleep 10


#     if sudo virsh dumpxml $instance | grep "hostdev"; then

#         curl -X POST https://$url/api/vmlog/ -d "level=20&virt_brick=$instance&message=GPU%20attached%20successfully."  # Logging

#     else

#         curl -X POST https://$url/api/vmlog/ -d "level=30&virt_brick=$instance&message=Attempting%20to%20attach%20GPU%20again."           # Logging

#         sudo virsh start $instance && 2>> bash_errors.log

#         sleep 10

#         sudo virsh attach-device $instance /home/bb_dev/GPU.xml && 2>> bash_errors.log

#         sleep 10

#         sudo virsh reboot $instance && 2>> bash_errors.log

#     fi


#     if sudo virsh dumpxml $instance | grep "hostdev"; then

#         curl -X POST https://$url/api/vmlog/ -d "level=20&virt_brick=$instance&message=GPU%20attached%20successfully."  # Logging

#     else

#         curl -X POST https://$url/api/vmlog/ -d "level=40&virt_brick=$instance&message=Failled%20to%20attach%20GPU."    # Logging

#     fi


#     sudo virsh start $instance && 2>> bash_errors.log

#     rm /home/bb_dev/GPU.xml 2>> bash_errors.log

#     curl https://dev.brickbox.io/vm/register/$instance/\$(sudo virsh domuuid $instance)/ &

#     echo "VM Cloned"

# else

#     curl -X POST https://dev.brickbox.io/vm/error/ -d "instance=$instance&error=clone" &

# fi

# exit

# EOF
