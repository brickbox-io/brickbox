#!/bin/bash

# Confirms that the host is ready for virtualization.

# Verify that QEMU is installed.
if [ ! -f /usr/bin/qemu-system-x86_64 ]; then
  echo "QEMU is not installed. Please install QEMU and try again."
  exit 1
fi

# Check that GPUs are set for VFIO.
