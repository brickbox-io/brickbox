#!/bin/bash

instance=$1

sshpass -p "Password@1" ssh -o StrictHostKeyChecking=no -p 9002 bb_dev@localhost << EOF

sleep 1

sudo virsh destroy $instance &&

sudo virsh undefine $instance &&

exit

EOF
