# box

Internal package that provides an API layer for managing hosts and virtual machines.

Assume sucess unless error.

## Background

Celery is used to manage the background tasks that include creating SSH connections. Each host should have its own celery worker process.

## Objects and Methods

| Object  | Method         | Description                                |
|---------|----------------|--------------------------------------------|
| Command | list_directory | List the contents of a directory on a host |
| Command | download_file  | Downloads a file from a URL to the host.   |

```python
host = box.Connect(
            host_port = #
        )

host.list_directory('directory/path')
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
