''' Tasks that can be called upon. '''

from __future__ import absolute_import, unicode_literals

import subprocess

from django.contrib.sites.models import Site

from celery import shared_task

import box

from bb_vm.models import (
    PortTunnel, VirtualBrick, HostFoundation
)

DIR = '/opt/brickbox/bb_vm/bash_scripts/'

# ---------------------------------------------------------------------------- #
#                                Scripted Tasks                                #
# ---------------------------------------------------------------------------- #

# -------------------------------- Shutdown VM ------------------------------- #
@shared_task
def pause_vm_subprocess(instance_id):
    '''
    Called to power down a VM.
    '''
    host = VirtualBrick.objects.get(id=instance_id).host
    virtual_machine = box.Brick(host_port=host.ssh_port, brick_id=f'{str(instance_id)}')
    virtual_machine.toggle_state(set_state="off")


# --------------------------------- Bootup VM -------------------------------- #
@shared_task
def play_vm_subprocess(instance_id):
    '''
    Resume VM from off state.
    '''
    host = VirtualBrick.objects.get(id=instance_id).host
    virtual_machine = box.Brick(host_port=host.ssh_port, brick_id=f'{str(instance_id)}')
    virtual_machine.toggle_state(set_state="on")

# --------------------------------- Reboot VM -------------------------------- #
@shared_task
def reboot_vm_subprocess(instance_id):
    '''
    Called to reboot a VM.
    '''
    host = VirtualBrick.objects.get(id=instance_id).host

    reboot_vm_script = [
                        f'{DIR}brick_connect.sh',
                        f'{str(host.ssh_username)}', f'{str(host.ssh_port)}',
                        'brick_reboot', f'{str(Site.objects.get_current().domain)}',
                        f'{str(instance_id)}',
                    ]
    with subprocess.Popen(reboot_vm_script) as script:
        print(script)


# --------------------------------- Delete VM -------------------------------- #
@shared_task
def destroy_vm_subprocess(instance_id, host_id=None):
    '''
    Called to destroy VM.
    '''

    if host_id is None:
        brick = VirtualBrick.objects.get(id=instance_id)
        host = brick.host
    else:
        host = HostFoundation.objects.get(id=host_id)

    virtual_machine = box.Brick(host_port=host.ssh_port, brick_id=f'{str(instance_id)}')
    virtual_machine.destroy()

    if host_id is None:
        brick.delete()

# ---------------------------- Terminate SSH Port ---------------------------- #
@shared_task
def close_ssh_port(port_number):
    '''
    Called when a VM is being destryed, a delay is set before the port becomes available again.
    '''
    PortTunnel.objects.filter(port_number=port_number).delete()
