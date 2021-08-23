''' Tasks that can be called upon. '''

from __future__ import absolute_import, unicode_literals

import subprocess

from celery import shared_task

from bb_vm.models import PortTunnel

DIR = '/opt/brickbox/bb_vm/bash_scripts/'

@shared_task
def new_vm_subprocess(instance_id, xml):
    '''
    Called to start the creation of a VM in the background.
    '''
    with subprocess.Popen([f'{DIR}clone_img.sh', f'{str(instance_id)}', f'{str(xml)}']) as script:
        print(script)


@shared_task
def pause_vm_subprocess(instance_id):
    '''
    Called to power down a VM.
    '''
    with subprocess.Popen([f'{DIR}brick_pause.sh', f'{str(instance_id)}']) as script:
        print(script)


@shared_task
def play_vm_subprocess(instance_id):
    '''
    Resume VM from off state.
    '''
    with subprocess.Popen([f'{DIR}brick_play.sh', f'{str(instance_id)}']) as script:
        print(script)


@shared_task
def reboot_vm_subprocess(instance_id):
    '''
    Called to reboot a VM.
    '''
    with subprocess.Popen([f'{DIR}brick_reboot.sh', f'{str(instance_id)}']) as script:
        print(script)

@shared_task
def destroy_vm_subprocess(instance_id):
    '''
    Called to destroy VM.
    '''
    with subprocess.Popen([f'{DIR}brick_destroy.sh', f'{str(instance_id)}']) as script:
        print(script)


@shared_task
def close_ssh_port(port_number):
    '''
    Called when a VM is being destryed, a delay is set before the port becomes available again.
    '''
    PortTunnel.objects.filter(port_number=port_number).delete()
