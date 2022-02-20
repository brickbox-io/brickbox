#!/bin/bash

url=$1
instance=$2

# ---------------------------------------------------------------------------- #
#                                    Logging                                   #
# ---------------------------------------------------------------------------- #
function log {
    log_file=brick_dhcp.log
    echo "$(date) - $1" >> $log_file
}

log "START - brick_dhcp.sh started with url=$url, instance=$instance"

sudo virt-customize -a /var/lib/libvirt/images/"$instance".img --run-command 'sudo dhclient -r enp105s0 && sudo dhclient enp105s0'
