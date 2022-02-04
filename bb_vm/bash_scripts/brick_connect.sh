#!/bin/bash

# Connects to a remote host through a SSH tunnel and runs the provided script.

# --------------------------------- Arguments -------------------------------- #

# $1: Remote (root) username
# $2: Host assigned port tunnel
# $3: The script that will be executed on the remote host

## The Following arguments are passed along to the script

# $4: URL Endpint
# $5: Instance ID that has been provided to refrence this new VM
# $6: XML formatted data to attach GPU to VM
#  7: DEBUG indicator (0 or 1) when using the flag option

DEBUG=0

# ---------------------------------------------------------------------------- #
#                                    Options                                   #
# ---------------------------------------------------------------------------- #

while getopts ":d" flags; do
  case "${flags}" in
    d) DEBUG=1;
    shift ;;
    \?) echo "Invalid option: -${OPTARG}" >&2;
    exit 1 ;;
  esac
done


# ---------------------------------------------------------------------------- #
#                                   Arguments                                  #
# ---------------------------------------------------------------------------- #

host_user=$1
port=$2
action=$3

url=$4
instance=$5
xml_data=$6
root_pass=$7


# ---------------------------------------------------------------------------- #

# Check that port is active before trying to connect.
if lsof -i tcp:"$port"; then

    # sudo cat /opt/brickbox/bb_vm/bash_scripts/"$action".sh "$url" "$instance" \""$xml_data"\" 2>> /opt/brickbox/bb_vm/bash_scripts/logs/brick_connect_errors.log) | sudo ssh -i /opt/brickbox/bb_vm/keys/"$host_user" -o StrictHostKeyChecking=no -p "$port" "$host_user"@localhost 'sudo bash -s' 2>> /opt/brickbox/bb_vm/bash_scripts/logs/brick_connect_errors.log
    ssh -i /opt/brickbox/bb_vm/keys/"$host_user" -o StrictHostKeyChecking=no -p "$port" "$host_user"@localhost 'sudo bash -s' < /opt/brickbox/bb_vm/bash_scripts/"$action".sh "$url" "$instance" \""$xml_data"\" "$root_pass" "$DEBUG" 2>> /opt/brickbox/bb_vm/bash_scripts/logs/brick_connect_errors.log

    curl -X POST https://"$url"/api/vmlog/ \
    -d "level=20" \
    -d "host=$port" \
    -d "virt_brick=$instance" \
    -d "message=Successfully connected to host via tunnel." \
    -d "command=ssh -i /opt/brickbox/bb_vm/keys/""$host_user"" -o StrictHostKeyChecking=no -p ""$port"" ""$host_user""@localhost 'sudo bash -s' < /opt/brickbox/bb_vm/bash_scripts/""$action"".sh ""$url"" ""$instance"" \"""$xml_data""\" ""$root_pass"" ""$DEBUG"" "

    exit 0

else

    curl -X POST https://"$url"/api/vmlog/ \
    -d "level=50" \
    -d "host=$port" \
    -d "virt_brick=$instance" \
    -d "message=Could not connect to host port." \
    -d "command=ssh -i /opt/brickbox/bb_vm/keys/""$host_user"" -o StrictHostKeyChecking=no -p ""$port"" ""$host_user""@localhost 'sudo bash -s' < /opt/brickbox/bb_vm/bash_scripts/""$action"".sh ""$url"" ""$instance"" \"""$xml_data""\" ""$root_pass"" ""$DEBUG"" "

    exit 1

fi
