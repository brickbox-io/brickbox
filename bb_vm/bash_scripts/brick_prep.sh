#!/bin/bash

# Confirms that the host is ready for virtualization.

# url=$1

# Verify that QEMU is installed.
if [ ! -f /usr/bin/qemu-system-x86_64 ]; then
    echo "QEMU is not installed. Attempting to install."
    # sudo apt-get install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils -y
    sudo apt-get install qemu-kvm qemu-utils libvirt-daemon-system libvirt-clients bridge-utils virt-manager ovmf -y
    # apt-get install qemu-kvm -y
    # sudo apt-get install qemu -y
    exit 1
fi

# Check if directory exists.
if [ ! -d "vfio-pci-bind/" ]; then
    sudo git clone https://github.com/andre-richter/vfio-pci-bind.git
fi

# Check that file is executable, if not, make it executable.
if [ ! -x /vfio-pci-bind/vfio-pci-bind ]; then
    sudo chmod +x vfio-pci-bind/vfio-pci-bind.sh
fi

# check if br0 exists, if not, create it.
if [ ! -d /sys/class/net/br0 ]; then
    sudo ip link add name br0 type bridge

    sudo ip link set dev br0 up
    sudo ip link set dev enp3s0f1 master br0

    sudo dhclient -r br0 && sudo dhclient br0
fi

# Verify that br0 has an IP address.
if [[ $(ip -f inet addr show br0) ]] ; then
    echo "br0 has an IP address."
else
    echo "br0 does not have an IP address."
    sudo dhclient -r br0 && sudo dhclient br0
fi


# Verify base image exists. (Need to change to long lasting task)
if [ ! -f /var/lib/libvirt/images/brickbox-U20.04.img ]; then
    curl https://os-imgs.nyc3.digitaloceanspaces.com/brickbox-U20.04.img \
    --output /var/lib/libvirt/images/brickbox-U20.04.img &
fi

# Verify that the XML file exists.
if [ ! -f /var/lib/libvirt/images/brickbox-U20.04.xml ]; then
    curl https://os-imgs.nyc3.digitaloceanspaces.com/brickbox-U20.04.xml \
    --output /var/lib/libvirt/images/brickbox-U20.04.xml && sudo virsh define /var/lib/libvirt/images/brickbox-U20.04.xml &
fi

sudo ip link set dev enp3s0f1 up
sudo dhclient -r enp3s0f1 && sudo dhclient enp3s0f1

sudo service gdm3 stop

sudo rmmod nvidia_uvm
sudo rmmod nvidia_drm
sudo rmmod nvidia_modeset
sudo rmmod nvidia

exit
