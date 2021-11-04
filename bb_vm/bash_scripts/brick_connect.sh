#!/bin/bash

# --------------------------------- Arguments -------------------------------- #
# - (1) URL Endpint
# - (2) Instance ID that has been provided to refrence this new VM.
# - (3) XML formatted data to attach GPU to VM

action_script=$1
url=$2
instance=$3
xml_data=$4
root_user=$5

if lsof -i tcp:9002; then

    sshpass -p "Password@1" ssh -i /opt/brickbox/bb_vm/keys/bb_root -o StrictHostKeyChecking=no -p 9002 "$root_user"@localhost 'bash -s' < /opt/brickbox/bb_vm/bash_scripts/"$action_script".sh "$url" "$instance" \""$xml_data"\" 2>> /opt/brickbox/bb_vm/bash_scripts/bash_errors.log

else

    curl -X POST https://"$url"/api/vmlog/ -d "level=50&virt_brick=$instance&message=Could%20not%20connect%20to%20host%20port." &

fi
