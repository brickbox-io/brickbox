#!/bin/bash

# --------------------------------- Arguments -------------------------------- #
# 1) Instance ID that has been provided to refrence this new VM.

instance=$1
xml_data=$2

sshpass -p "Password@1" ssh -p 9002 bb_dev@localhost << EOF

sleep 1

rm /home/bb_dev/GPU.xml 2>> bash_errors.log

sudo virt-clone --original brickbox-U20.04 --name $instance --auto-clone &&

sudo virsh start $instance &&

echo "$xml_data" >> GPU.xml 2>> bash_errors.log

sudo virsh attach-device $instance GPU.xml 2>> bash_errors.log

rm /home/bb_dev/GPU.xml 2>> bash_errors.log

curl https://dev.brickbox.io/vm/register/$instance/\$(sudo virsh domuuid $instance)/ &

echo "VM Cloned"

exit

EOF
