#!/bin/bash

url=$1
img_name=$2
img_url=$3

# ---------------------------------------------------------------------------- #
#                                    Logging                                   #
# ---------------------------------------------------------------------------- #

function log {
    log_file=host_download_base_img.log
    echo "$(date) - $1" >> $log_file
}

log "START - host_download_base_img.sh started with url $url. Downloading $img_name from $img_url" # Logging

# ---------------------------------- Actions --------------------------------- #
curl "$img_url" --output /var/lib/libvirt/images/"$img_name" &

exit 0
