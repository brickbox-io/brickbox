''' Tasks that support overall system operations. '''

from subprocess import Popen, PIPE

from django.conf import settings
from django.contrib.sites.models import Site

from celery import shared_task

from bb_vm.models import PortTunnel, HostFoundation, GPU, VirtualBrick

# Script directory on server.
DIR = '/opt/brickbox/bb_vm/bash_scripts/'

@shared_task
def prepare_gpu_background_task():
    '''
    Cycles through available GPUs to confirm all have background VM ready to launch.
    '''

    gpu_list = GPU.objects.filter(host=host)
    for gpu in gpu_list:
        if not gpu.bg_ready and not gpu.is_rented and gpu.host.is_ready:
            clone_bg.apply_async((gpu.id,), queue='ssh_queue')
            gpu_list.update(bg_ready=True)

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
