''' Tasks that can be called upon. '''

from __future__ import absolute_import, unicode_literals

import subprocess

from django.contrib.sites.models import Site

from celery import shared_task

from bb_vm.models import (
    PortTunnel, VirtualBrickOwner, VirtualBrick,
)

DIR = '/opt/brickbox/bb_vm/bash_scripts/'

# ---------------------------------------------------------------------------- #
#                                Scripted Tasks                                #
# ---------------------------------------------------------------------------- #

@shared_task
def new_vm_subprocess(instance_id, xml, root_user):
    '''
    Called to start the creation of a VM in the background.
    '''
    catch_clone_errors.apply_async((instance_id,), countdown=60)
    remove_stale_clone.apply_async((instance_id,), countdown=180)

    new_vm_script = [
                        f'{DIR}brick_connect.sh',
                        'brick_img',
                        f'{str(Site.objects.get_current().domain)}',
                        f'{str(instance_id)}',
                        f'{str(xml)}',
                        f'{str(root_user)}'
                    ]
    with subprocess.Popen(new_vm_script) as script:
        print(script)


@shared_task
def pause_vm_subprocess(instance_id, root_user):
    '''
    Called to power down a VM.
    '''
    pause_vm_script = [
                        f'{DIR}brick_connect.sh',
                        'brick_pause',
                        f'{str(Site.objects.get_current().domain)}',
                        f'{str(instance_id)}',
                        f'{str(root_user)}'
                    ]
    with subprocess.Popen(pause_vm_script) as script:
        print(script)

    # with subprocess.Popen([f'{DIR}brick_pause.sh', f'{str(instance_id)}']) as script:
    #     print(script)


@shared_task
def play_vm_subprocess(instance_id, root_user):
    '''
    Resume VM from off state.
    '''
    play_vm_script = [
                        f'{DIR}brick_connect.sh',
                        'brick_play',
                        f'{str(Site.objects.get_current().domain)}',
                        f'{str(instance_id)}',
                        f'{str(root_user)}'
                    ]
    with subprocess.Popen(play_vm_script) as script:
        print(script)

    # with subprocess.Popen([f'{DIR}brick_play.sh', f'{str(instance_id)}']) as script:
    #     print(script)


@shared_task
def reboot_vm_subprocess(instance_id, root_user):
    '''
    Called to reboot a VM.
    '''
    reboot_vm_script = [
                        f'{DIR}brick_connect.sh',
                        'brick_reboot',
                        f'{str(Site.objects.get_current().domain)}',
                        f'{str(instance_id)}',
                        f'{str(root_user)}'
                    ]
    with subprocess.Popen(reboot_vm_script) as script:
        print(script)

    # with subprocess.Popen([f'{DIR}brick_reboot.sh', f'{str(instance_id)}']) as script:
    #     print(script)


@shared_task
def destroy_vm_subprocess(instance_id, root_user):
    '''
    Called to destroy VM.
    '''
    destroy_vm_script = [
                        f'{DIR}brick_connect.sh',
                        'brick_destroy',
                        f'{str(Site.objects.get_current().domain)}',
                        f'{str(instance_id)}',
                        f'{str(root_user)}'
                    ]
    with subprocess.Popen(destroy_vm_script) as script:
        print(script)

    # with subprocess.Popen([f'{DIR}brick_destroy.sh', f'{str(instance_id)}']) as script:
    #     print(script)


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
    brick = VirtualBrick.objects.get(id=instance_id)
    if brick.ssh_port is None and brick.is_on is False:
        VirtualBrickOwner.objects.filter(virt_brick=instance_id).delete()
        brick.delete()
        destroy_vm_subprocess(instance_id, brick.host.ssh_usernmae)
