#!/bin/bash

# Starts a brick up that is shutdown.

url=$1
instance=$2


sleep 1

sudo virsh start $instance

exit
