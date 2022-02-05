#!/bin/bash

url=$1
host=$2

files=$(sudo ls /var/lib/libvirt/images/)

curl -X POST https://"$url"/vm/host/garbage/"$host"/ \
-d "files=$files"

exit 0
