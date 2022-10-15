''' Contains all tasks for initialising a new VM (brick) '''

from __future__ import absolute_import, unicode_literals

import json
import subprocess

from django.contrib.sites.models import Site

from celery import shared_task
import box

from bb_vm.models import (
    VirtualBrickOwner, VirtualBrick, RentedGPU,
)


DIR = '/opt/brickbox/bb_vm/bash_scripts/'

# ---------------------------------- New VM ---------------------------------- #
@shared_task
def new_vm_subprocess(instance_id, root_pass, os_version=1):
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

    virtual_machine = box.Brick(host_port=host.ssh_port, brick_id=f'{str(instance_id)}')

    try:
        # ------------------------------------- 1 ------------------------------------ #
        if brick.user_data is not None:
            virtual_machine.user_data = brick.user_data.script

        virtual_machine.create(base_image=f"base_os-{os_version}")

        brick.domain_uuid = virtual_machine.domuuid()
        brick.img_cloned = True
        brick.save()

        # ------------------------------------- 2 ------------------------------------ #
        virtual_machine.set_root_password(password=f'{str(root_pass)}')

        # ------------------------------------- 3 ------------------------------------ #
        for owner in brick.owners.all():
            for key in owner.keys.all():
                virtual_machine.set_ssh_key(key=f'{str(key.pub_key)}')

        # ------------------------------------- 4 ------------------------------------ #
        gpu_xml = RentedGPU.objects.filter(virt_brick=brick)[0].gpu.xml
        virtual_machine.attach_gpu(xml_data=f'{str(gpu_xml)}')

        # ------------------------------------- 5 ------------------------------------ #
        virtual_machine.toggle_state(set_state='on')

    except IndexError as err:
        print(err)


    finally:
        catch_clone_errors.apply_async((instance_id,), countdown=600, queue='ssh_queue')
        remove_stale_clone.apply_async((instance_id,), countdown=1560, queue='ssh_queue')


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

            brick = VirtualBrick.objects.get(id=instance_id)
            host = brick.host

            destroy_vm_script = [
                        f'{DIR}brick_connect.sh',
                        f'{str(host.ssh_username)}', f'{str(host.ssh_port)}',
                        'brick_destroy', f'{str(Site.objects.get_current().domain)}',
                        f'{str(instance_id)}',
                    ]

            with subprocess.Popen(destroy_vm_script) as script:
                print(script)

        return True

    except VirtualBrick.DoesNotExist as err:
        return json.dumps({
            'error':f'{err}'
        })
