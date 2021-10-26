#!/bin/bash

# This script pauses the brick by shutting it down.

url=$1
instance=$2


sleep 1

sudo virsh shutdown  "$instance"

exit
