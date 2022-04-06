
To view the structure of a VM use the `qemu-img info {img}` command.

## Storage

```bash
# Resize an image
qemu-img resize /path/to/image.img +10G

# From within the VM
cd /etc/netplan
growpart /dev/vda 1
resize2fs /dev/vda1
```

## GPU Pass Through

To bind vfio used [this tool](https://github.com/andre-richter/vfio-pci-bind/blob/master/vfio-pci-bind.sh). Refrence [this guide](https://mathiashueber.com/pci-passthrough-ubuntu-2004-virtual-machine/) or [this video](https://www.youtube.com/watch?v=3yhwJxWSqXI&ab_channel=ChrisTitusTech) for more information on PCI passthrough.

```bash
# Find PCIe IDs
lspci -nn -D | grep -iP "VGA|audio"
lspci -vnn | grep -iP "vga|amdgpu|nvidia|nouveau|vfio-pci"

# Bind each card to vfio-pci
vfio-pci-bind.sh Vendor:Device Domain:Bus:Device.Function
```
