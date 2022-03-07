#!/bin/bash

url=$1
host=$2

# ---------------------------------------------------------------------------- #
#                                    Logging                                   #
# ---------------------------------------------------------------------------- #

function log {
    log_file=host_base_img.log
    echo "$(date) - $1" >> $log_file
}

log "START - host_base_img.sh started with url $url and host $host" # Logging

# ---------------------------------- Actions --------------------------------- #

files=$(sudo ls /var/lib/libvirt/images/)

log "Files Found: $files" # Logging

curl -X POST https://"$url"/vm/host/check/base_imgs/"$host"/ \
-d "files=$files"

log "END - host_cleanup.sh ended" # Logging

exit 0
