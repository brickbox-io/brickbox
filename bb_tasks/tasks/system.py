''' Tasks that support overall system operations. '''

import subprocess

from django.contrib.sites.models import Site

from celery import shared_task
import box

from bb_vm.models import GPU, BackgroundTask

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
            host = gpu.host

            background_brick = box.Brick(host_port=host.ssh_port, brick_id=f'gpu_{str(gpu.id)}')
            background_brick.USER_DATA = BackgroundTask.objects.all().order_by('-id')[0].script

            background_brick.create(base_image="base_os-1")
            background_brick.set_root_password(password=f'r0flduqu')
            background_brick.attach_gpu(xml_data=f'{str(gpu.xml)}')
            background_brick.toggle_state(set_state='on')

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
