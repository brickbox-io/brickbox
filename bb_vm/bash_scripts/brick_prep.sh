#!/bin/bash

# Confirms that the host is ready for virtualization.

# url=$1

# Verify that QEMU is installed.
if [ ! -f /usr/bin/qemu-system-x86_64 ]; then
  echo "QEMU is not installed. Please install QEMU and try again."
  exit 1
fi

# Check if directory exists.
if [ ! -d "/vfio-pci-bind" ]; then
    sudo git clone https://github.com/andre-richter/vfio-pci-bind.git
fi

# Check that file is executable, if not, make it executable.
if [ ! -x /vfio-pci-bind/vfio-pci-bind ]; then
    sudo chmod +x /vfio-pci-bind/vfio-pci-bind.sh
fi

exit
