#!/bin/bash

url=$1
instance=$2
key=$3
root_pass=$4


# ---------------------------------------------------------------------------- #
#                                    Logging                                   #
# ---------------------------------------------------------------------------- #
function log {
    log_file=brick_auth.log
    echo "$(date) - $1" >> $log_file
}

log "START - brick_auth.sh started with url=$url, instance=$instance"

# Remote Logging
curl -X POST https://"$url"/api/vmlog/ \
-d "level=20" \
-d "virt_brick=$instance" \
-d "message=Adding brick authentication."

if [ "$root_pass" != '0' ]; then
    log "root_pass is set to true, adding root password"
    sudo virt-customize -a /var/lib/libvirt/images/"$instance".img --root-password password:"$root_pass" 2>> bash_errors.log

elif [ "$key" != '0' ]; then
    log "key is set, adding ssh key: $key"
    sudo echo "$key" | sudo tee -a ssh.key > /dev/null 2>> bash_errors.log
    sudo virt-customize -a /var/lib/libvirt/images/"$instance".img --ssh-inject root:file:ssh.key 2>> bash_errors.log
    sudo rm ssh.key 2>> bash_errors.log

fi
log "END - brick_auth.sh ended"

exit 0
