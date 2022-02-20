''' Contains all tasks for initialising a new VM (brick) '''

from __future__ import absolute_import, unicode_literals

import json
import subprocess

from django.contrib.sites.models import Site

from celery import shared_task

from bb_vm.models import (
    VirtualBrickOwner, VirtualBrick, RentedGPU,
)

DIR = '/opt/brickbox/bb_vm/bash_scripts/'

# ---------------------------------- New VM ---------------------------------- #
@shared_task
def new_vm_subprocess(instance_id, root_pass):
    '''
    Called to start the creation of a VM in the background.
    1) Create base VM image
    2) Set root password
    3) Add SSH Keys
    4) Attach GPU
    5) Boot VM
    '''
    brick = VirtualBrick.objects.get(id=instance_id)
    host = brick.host
    try:
        # ------------------------------------- 1 ------------------------------------ #
        brick_clone = [
                            f'{DIR}brick_connect.sh',
                            f'{str(host.ssh_username)}', f'{str(host.ssh_port)}',
                            'initialise/brick_clone', f'{str(Site.objects.get_current().domain)}',
                            f'{str(instance_id)}', 'NONE', 'NONE',
                        ]
        with subprocess.Popen(brick_clone) as script:
            print(script)

        if not VirtualBrick.objects.get(id=instance_id).img_cloned:
            return

        # ------------------------------------- 2 ------------------------------------ #
        brick_auth = [
                            f'{DIR}brick_connect.sh',
                            f'{str(host.ssh_username)}', f'{str(host.ssh_port)}',
                            'initialise/brick_auth', f'{str(Site.objects.get_current().domain)}',
                            f'{str(instance_id)}', '0', f'{str(root_pass)}',
                        ]
        with subprocess.Popen(brick_auth) as script:
            print(script)

        # ------------------------------------- 3 ------------------------------------ #
        for owner in brick.owners.all():
            for key in owner.keys.all():
                brick_auth = [
                            f'{DIR}brick_connect.sh',
                            f'{str(host.ssh_username)}', f'{str(host.ssh_port)}',
                            'initialise/brick_auth', f'{str(Site.objects.get_current().domain)}',
                            f'{str(instance_id)}', f'{str(key.pub_key)}', '0',
                        ]
            with subprocess.Popen(brick_auth) as script:
                print(script)

        # ------------------------------------- 4 ------------------------------------ #
        gpu_xml = RentedGPU.objects.filter(virt_brick=brick)[0].gpu.xml

        brick_gpu = [
                            f'{DIR}brick_connect.sh',
                            f'{str(host.ssh_username)}', f'{str(host.ssh_port)}',
                            'initialise/brick_gpu', f'{str(Site.objects.get_current().domain)}',
                            f'{str(instance_id)}', f'{str(gpu_xml)}', 'NONE',
                        ]
        with subprocess.Popen(brick_gpu) as script:
            print(script)

        # ------------------------------------- 5 ------------------------------------ #
        brick_boot = [
                        f'{DIR}brick_connect.sh',
                            f'{str(host.ssh_username)}', f'{str(host.ssh_port)}',
                            'initialise/brick_boot', f'{str(Site.objects.get_current().domain)}',
                            f'{str(instance_id)}', 'NONE', 'NONE',
                        ]
        with subprocess.Popen(brick_boot) as script:
            print(script)

    except IndexError as err:
        print(err)


    finally:
        catch_clone_errors.apply_async((instance_id,), countdown=240, queue='ssh_queue')
        remove_stale_clone.apply_async((instance_id,), countdown=720, queue='ssh_queue')


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
