''' Structure folder as importable app for tasks. '''

from .periodic import verify_host_connectivity
from .callable import (
    new_vm_subprocess, pause_vm_subprocess, play_vm_subprocess,
    reboot_vm_subprocess, destroy_vm_subprocess, close_ssh_port,
    catch_clone_errors, remove_stale_clone
)

__all__ = [
    'verify_host_connectivity',
    'new_vm_subprocess', 'pause_vm_subprocess', 'play_vm_subprocess',
    'reboot_vm_subprocess', 'destroy_vm_subprocess', 'close_ssh_port',
    'catch_clone_errors', 'remove_stale_clone'
]
