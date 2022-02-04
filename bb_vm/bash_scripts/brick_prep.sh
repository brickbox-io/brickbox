#!/bin/bash

# Confirms that the host is ready for virtualization.

# url=$1 (NOT USED)

# Flags
DEBUG=$5 # -d

# ---------------------------------------------------------------------------- #
#                                    Logging                                   #
# ---------------------------------------------------------------------------- #

function log {
    log_file=brick_prep.log
    echo "$(date) - $1" >> $log_file
}

log "START - brick_prep.sh started with DEBUG=$DEBUG"


if [ "$DEBUG" -eq 1 ]; then
    os_url='https://os-imgs.nyc3.digitaloceanspaces.com/dev-brickbox-U20.04.img'
elif [ "$DEBUG" -eq 0 ]; then
    os_url='https://os-imgs.nyc3.digitaloceanspaces.com/brickbox-U20.04.img'
fi


# ---------------------------------------------------------------------------- #
#                            Verification Processes                            #
# ---------------------------------------------------------------------------- #

# Verify that QEMU is installed.
if [ ! -f /usr/bin/qemu-system-x86_64 ]; then
    log "QEMU is not installed. Attempting to install." # Logging
    sudo apt-get install qemu-kvm qemu-utils libvirt-daemon-system libvirt-clients bridge-utils virt-manager ovmf libguestfs-tools -y
    # exit 1
fi

# Check if pci binding tool directory exists.
if [ ! -d "vfio-pci-bind/" ]; then
    log "vfio-pci-bind/ directory does not exist. Attempting to clone." # Logging
    sudo git clone https://github.com/andre-richter/vfio-pci-bind.git
fi

# Check that file is executable, if not, make it executable.
if [ ! -x /home/bb_root/vfio-pci-bind/vfio-pci-bind.sh ]; then
    log "vfio-pci-bind/vfio-pci-bind is not executable. Attempting to make it executable." # Logging
    sudo chmod +x vfio-pci-bind/vfio-pci-bind.sh
fi

# -------------------------------- Networking -------------------------------- #

# sudo ip link set dev enp3s0f1 up
# sudo dhclient -r enp3s0f1 && sudo dhclient enp3s0f1
# use "ip route show" to see the routes
# ip route del default via 0.0.0.0 dev enp3s0f1

# check if br0 exists, if not, create it.
if [ ! -d /sys/class/net/br0 ]; then
    log "br0 does not exist. Attempting to create." # Logging
    sudo ip link add name br0 type bridge
    sudo ip link set dev br0 up && sudo ip link set dev enp3s0f1 master br0
    #sudo dhclient -r br0 && sudo dhclient br0
fi

# Verify that enp3s0f1 is up.
if [[ $(ip -f inet addr show enp3s0f1) ]] ; then
    log "enp3s0f1 is up." # Logging
else
    log "enp3s0f1 is not up. Attempting to bring it up." # Logging
    sudo ip link set dev enp3s0f1 up
    sudo dhclient -r enp3s0f1 && sudo dhclient enp3s0f1
    sudo ip route del default dev enp3s0f1 # Remove default route (TESTING)

fi

# Verify that br0 has an IP address.
if [[ $(ip -f inet addr show br0) ]] ; then
    log "br0 has an IP address." # Logging
else
    log "br0 does not have an IP address. Attempting to assign one." # Logging
    sudo dhclient -r br0 && sudo dhclient br0
fi


# Verify base image exists. (Need to change to long lasting task)
if [ ! -f /var/lib/libvirt/images/brickbox-U20.04.img ]; then
    log "Base img does not exist. Attempting to download." # Logging
    curl "$os_url" --output /var/lib/libvirt/images/brickbox-U20.04.img &
fi

# Verify that the XML file exists.
if [ ! -f /var/lib/libvirt/images/brickbox-U20.04.xml ]; then
    log "XML file does not exist. Attempting to create." # Logging
    curl https://os-imgs.nyc3.digitaloceanspaces.com/brickbox-U20.04.xml \
    --output /var/lib/libvirt/images/brickbox-U20.04.xml && sudo virsh define /var/lib/libvirt/images/brickbox-U20.04.xml &
fi

# sudo ip link set dev enp3s0f1 up
# sudo dhclient -r enp3s0f1 && sudo dhclient enp3s0f1

sudo service gdm3 stop

sudo rmmod nvidia_uvm
sudo rmmod nvidia_drm
sudo rmmod nvidia_modeset
sudo rmmod nvidia

log "END" # Logging
exit 0
