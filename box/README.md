# box

Internal package that provides an API layer for managing hosts and virtual machines.

## Background

Celery is used to manage the background tasks that include creating SSH connections. Each host should have its own celery worker process.

## Objects and Methods

| Object  | Method         | Description                                |
|---------|----------------|--------------------------------------------|
| Command | list_directory | List the contents of a directory on a host |
| Command | download_file  | Downloads a file from a URL to the host.   |
