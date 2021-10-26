#!/bin/bash

# Restarts the virtual brick.

url=$1
instance=$2

sleep 1

sudo virsh reboot $instance

exit
