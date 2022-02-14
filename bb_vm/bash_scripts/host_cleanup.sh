#!/bin/bash

url=$1
host=$2

# ---------------------------------------------------------------------------- #
#                                    Logging                                   #
# ---------------------------------------------------------------------------- #

function log {
    log_file=host_cleanup.log
    echo "$(date) - $1" >> $log_file
}

log "START - host_cleanup.sh started with url $url and host $host" # Logging

# ---------------------------------- Actions --------------------------------- #

files=$(sudo ls /var/lib/libvirt/images/)

log "Files Found: $files" # Logging

curl -X POST https://"$url"/vm/host/garbage/"$host"/ \
-d "files=$files"

log "END - host_cleanup.sh ended" # Logging

exit 0
