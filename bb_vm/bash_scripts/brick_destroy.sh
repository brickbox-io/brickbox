#!/bin/bash

# Need to change folder permissions
# sudo chown -R bb_dev boot/


instance=$1

sshpass -p "Password@1" ssh -o StrictHostKeyChecking=no -p 9002 bb_dev@localhost << EOF

sleep 1

sudo virsh shutdown  $instance &&

sudo virsh destroy $instance &&

sudo virsh undefine $instance &&

sleep 5

sudo -n rm /var/lib/libvirt/images/$instance.qcow2 2>> bash_errors.log

sudo -n rm /var/lib/libvirt/images/$instance.img 2>> bash_errors.log

exit

EOF
