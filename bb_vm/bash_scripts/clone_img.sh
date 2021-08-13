#!/bin/bash

# --------------------------------- Arguments -------------------------------- #
# 1) Instance ID that has been provided to refrence this new VM.

instance=$1
xml_data=$2

sshpass -p "Password@1" ssh -p 9002 bb_dev@localhost << EOF

sleep 1

sudo virt-clone --original Test_Server --name $instance --auto-clone &&

sudo virsh start $instance &&

echo "$xml_data" >> GPU.xml

sudo virsh attach-device $instance GPU.xml

sudo rm GPU.xml

curl https://dev.brickbox.io/vm/register/$instance/\$(sudo virsh domuuid $instance)/ &

exit

EOF
