## Initialization

The following goes over the functional flow of creating VM once a host has been added to brickbox.io

## Logging

To aid in debugging the following standards are used:

| Action       | Logging Method                        |
|--------------|---------------------------------------|
| Bash Scripts | bb_root > file_name.log (on the host) |

## Host Connection Self Test

A host that is offline will dysplay **is_online** and **is_ready** as false. Reffer to the selection on keep alive for more information regarding online status. The **is_ready** status is managed by the *recconnect_host* periodic task.

### Host Prep (recconnect_host)

The host_prep script is ran whenever the host reconnects back to brickbox.io it is used to configure the networking interfaces and setup the GPUs for a VM.

## GPU Management

When the host is powered on any un-rented GPUs are tested.
