''' bb_vm - tasks.py '''

from __future__ import absolute_import, unicode_literals

import re

from celery import shared_task

import box


from bb_vm.models import HostFoundation, CloudImage

# Script directory on server.
DIR = '/opt/brickbox/bb_vm/bash_scripts/'

@shared_task
def check_base_imgs():
    '''
    Checks that each host contains all the base images defined by the CloudImage Model.
    '''
    hosts = HostFoundation.objects.filter(is_enabled=True, is_ready=True)

    for host in hosts:
        box.host_port = host.ssh_port
        files = box.Command.list_directory(
                            directory = '/var/lib/libvirt/images/'
                        )
        files_names = re.findall(r'base_os-(\d)+\.img', files.decode('utf-8'))

        for os_id in CloudImage.objects.filter(is_active=True):
            if not str(os_id.id) in files_names:
                files =  box.Command.download_file(
                        file_url = f'{os_id.img_url}',
                        file_path = '/var/lib/libvirt/images/',
                        file_name = f'base_os-{str(os_id.id)}.img',
                    )
