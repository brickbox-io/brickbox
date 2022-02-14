''' Tasks that can be called upon. '''

from __future__ import absolute_import, unicode_literals

import json
import subprocess
from typing import final

from django.contrib.sites.models import Site

from celery import shared_task

from bb_vm.models import (
    PortTunnel, VirtualBrickOwner, VirtualBrick, RentedGPU, HostFoundation
)

DIR = '/opt/brickbox/bb_vm/bash_scripts/'

# ---------------------------------------------------------------------------- #
#                                Scripted Tasks                                #
# ---------------------------------------------------------------------------- #

# ---------------------------------- New VM ---------------------------------- #
@shared_task
def new_vm_subprocess(instance_id, root_pass):
    '''
    Called to start the creation of a VM in the background.
    '''
    brick = VirtualBrick.objects.get(id=instance_id)
    host = brick.host

    try:
        gpu_xml = RentedGPU.objects.filter(virt_brick=brick)[0].gpu.xml

        new_vm_script = [
                            f'{DIR}brick_connect.sh',
                            f'{str(host.ssh_username)}', f'{str(host.ssh_port)}',
                            'brick_img', f'{str(Site.objects.get_current().domain)}',
                            f'{str(instance_id)}', f'{str(gpu_xml)}', f'{str(root_pass)}',
                        ]

        with subprocess.Popen(new_vm_script) as script:
            print(script)

    except IndexError as err:
        print(err)

    finally:
        catch_clone_errors.apply_async((instance_id,), countdown=120, queue='ssh_queue')
        remove_stale_clone.apply_async((instance_id,), countdown=360, queue='ssh_queue')


# -------------------------------- Shutdown VM ------------------------------- #
@shared_task
def pause_vm_subprocess(instance_id):
    '''
    Called to power down a VM.
    '''
    host = VirtualBrick.objects.get(id=instance_id).host

    pause_vm_script = [
                        f'{DIR}brick_connect.sh',
                        f'{str(host.ssh_username)}', f'{str(host.ssh_port)}',
                        'brick_pause', f'{str(Site.objects.get_current().domain)}',
                        f'{str(instance_id)}'
                    ]

    with subprocess.Popen(pause_vm_script) as script:
        print(script)


# --------------------------------- Bootup VM -------------------------------- #
@shared_task
def play_vm_subprocess(instance_id):
    '''
    Resume VM from off state.
    '''
    host = VirtualBrick.objects.get(id=instance_id).host

    play_vm_script = [
                        f'{DIR}brick_connect.sh',
                        f'{str(host.ssh_username)}', f'{str(host.ssh_port)}',
                        'brick_play', f'{str(Site.objects.get_current().domain)}',
                        f'{str(instance_id)}',
                    ]

    with subprocess.Popen(play_vm_script) as script:
        print(script)


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

    destroy_vm_script = [
                        f'{DIR}brick_connect.sh',
                        f'{str(host.ssh_username)}', f'{str(host.ssh_port)}',
                        'brick_destroy', f'{str(Site.objects.get_current().domain)}',
                        f'{str(instance_id)}',
                    ]


    with subprocess.Popen(destroy_vm_script) as script:
        print(script)

    brick.delete()

# ---------------------------- Terminate SSH Port ---------------------------- #
@shared_task
def close_ssh_port(port_number):
    '''
    Called when a VM is being destryed, a delay is set before the port becomes available again.
    '''
    PortTunnel.objects.filter(port_number=port_number).delete()


# ---------------------------------------------------------------------------- #
#                              Verification Tasks                              #
# ---------------------------------------------------------------------------- #

@shared_task
def catch_clone_errors(instance_id):
    '''
    Called when clone is requested, cleans up database if clone fails.
    '''
    brick = VirtualBrick.objects.get(id=instance_id)
    if brick.ssh_port is None and brick.img_cloned is False:
        VirtualBrickOwner.objects.filter(virt_brick=instance_id).delete()
        brick.delete()


@shared_task
def remove_stale_clone(instance_id):
    '''
    Last resort to remove clones that did not sucessfully start and never given a port.
    '''
    try:
        brick = VirtualBrick.objects.get(id=instance_id)

        if brick.ssh_port is None and brick.is_on is False:
            VirtualBrickOwner.objects.filter(virt_brick=instance_id).delete()
            brick.delete()
            destroy_vm_subprocess(instance_id)

        return True

    except VirtualBrick.DoesNotExist as err:
        return json.dumps({
            'error':f'{err}'
        })
