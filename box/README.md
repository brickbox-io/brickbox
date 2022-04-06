# box

Internal package that provides an API layer for managing hosts and virtual machines.

Assume sucess unless error.

## Background

Celery is used to manage the background tasks that include creating SSH connections. Each host should have its own celery worker process.

## Objects and Methods

| Object     | Method               | Description                                                            |
|------------|----------------------|------------------------------------------------------------------------|
| Command    | list_directory       | List the contents of a directory on a host                             |
| Command    | download_file        | Downloads a file from a URL to the host.                               |
| HostStatus | is_ready             | Returns true if the host is ready to use.                              |
| HostStatus | qemu_installed       | Returns true if qemu is installed on the host.                         |
| HostStatus | vfio_pci_bind_exists | Returns true if the vfio-pci-bind kernel module is loaded on the host. |
| HostStatus | br0_exists           | Returns true if the br0 interface exists on the host.                  |
| HostStatus | enp3s0f1_is_up       | Returns true if the enp3s0f1 interface is up on the host.              |
| HostStatus | br0_is_networked     | Returns true if the br0 interface is networked on the host.            |

```python
host = box.Connect(
            host_port = #
        )

# List the contents of a directory on a host
directory_contense = host.list_directory('directory/path')

# Download a file from a URL to the host
host.download_file('http://www.example.com/file.txt', 'file.txt', 'directory/path', 'File Name')
```

## VM Scripts

Scripts that need to be ran on the virtual machines by either the platform or the end user need to be uploaded to a file server. The scripts are then downloaded to the VM via CURL, and then executed.

## Cloud-Init

### Vendor Data

Using the cloud-init system a vendor-data file is created that contains runcmd to curl the scripts from the file server and then execute them.

### User Data

Userdata can be in the form of a YML file or start with `#! /bin/bash` to be executed as a script. It is ran when the image is initialized.

## Virtual Machine Configuration

SSH

| Categorey | Action             | Description                    | Location   |
|-----------|--------------------|--------------------------------|------------|
| SSH       | PermitRootLogin    | Allow root login with password | vm_init.sh |
| SSH       | AuthorizedKeysFile |                                | vm_init.sh |

## Examples

```python
import box

vm_box = box.Connect(
            host_port = #
        )
```

## Custimization

The message of the day (motd) can be customized with [ASCI text](https://patorjk.com/software/taag/#p=testall&f=Big%20Money-nw&t=brickbox.io).

```bash
cd /etc/update-motd.d/
```


Retreave system serial https://kb.mit.edu/confluence/pages/viewpage.action?pageId=152578725

https://serverfault.com/questions/401704/how-do-i-make-a-persistent-domain-with-virsh

https://askubuntu.com/questions/1166317/module-nvidia-is-in-use-but-there-are-no-processes-running-on-the-gpu https://linuxconfig.org/how-to-disable-blacklist-nouveau-nvidia-driver-on-ubuntu-20-04-focal-fossa-linux
