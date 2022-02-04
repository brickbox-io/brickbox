#!/bin/bash

echo "$1" >> ~sshtunnel/.ssh/expired_keys

sed -i "\:$1:d" ~sshtunnel/.ssh/authorized_keys
