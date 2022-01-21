''' Tasks that support overall system operations. '''

import subprocess

from django.contrib.sites.models import Site

from celery import shared_task

from bb_vm.models import GPU

# Script directory on server.
DIR = '/opt/brickbox/bb_vm/bash_scripts/'


@shared_task
def prepare_gpu_background_task():
    '''
    Cycles through available GPUs to confirm all have background VM ready to launch.
    '''
    gpu_list = GPU.objects.all()
    for gpu in gpu_list:
        if not gpu.bg_ready and not gpu.rented and gpu.host.is_ready:
            clone_bg.apply_async((gpu.id,), queue='ssh_queue')


@shared_task
def clone_bg(gpu_id):
    '''
    Called to create the background img for a particular GPU.
    '''
    gpu = GPU.objects.get(id=gpu_id)
    gpu_xml = gpu.xml
    host = gpu.host

    new_vm_script = [
                        f'{DIR}brick_connect.sh',
                        f'{str(host.ssh_username)}', f'{str(host.ssh_port)}',
                        'background_img', f'{str(Site.objects.get_current().domain)}',
                        f'gpu_{str(gpu.id)}', f'{str(gpu_xml)}'
                    ]

    with subprocess.Popen(new_vm_script) as script:
        print(script)

    gpu.bg_ready = True
    gpu.bg_running = True
    gpu.save()



@shared_task
def stop_bg(gpu_id):
    '''
    Called to stop the background img for a particular GPU.
    '''
    gpu = GPU.objects.get(id=gpu_id)
    host = gpu.host

    stop_bg_script = [
                        f'{DIR}brick_connect.sh',
                        f'{str(host.ssh_username)}', f'{str(host.ssh_port)}',
                        'brick_pause', f'{str(Site.objects.get_current().domain)}',
                        f'gpu_{str(gpu_id)}'
                    ]

    with subprocess.Popen(stop_bg_script) as script:
        print(script)

    gpu.bg_running = False
    gpu.save()


@shared_task
def start_bg(gpu_id):
    '''
    Called to start the background img for a particular GPU.
    '''
    gpu = GPU.objects.get(id=gpu_id)
    host = gpu.host

    resume_bg_script = [
                        f'{DIR}brick_connect.sh',
                        f'{str(host.ssh_username)}', f'{str(host.ssh_port)}',
                        'brick_play', f'{str(Site.objects.get_current().domain)}',
                        f'gpu_{str(gpu_id)}'
                    ]

    with subprocess.Popen(resume_bg_script) as script:
        print(script)

    gpu.bg_running = True
    gpu.save()
