#!/bin/bash

echo command="echo 'Port forwarding only account.'",no-pty "$1" >> ~sshtunnel/.ssh/authorized_keys
