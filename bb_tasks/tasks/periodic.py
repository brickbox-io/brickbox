''' Tasks that are setup to run continiously in the background. '''

from __future__ import absolute_import, unicode_literals

import json

from subprocess import Popen, PIPE

from celery import shared_task

from bb_vm.models import HostFoundation


@shared_task
def verify_host_connectivity():
    '''
    Checks that hosts are connected by cycling through ports to verify activity.
    '''
    hosts = HostFoundation.objects.all()

    port_result = False
    script = False

    for host in hosts:
        command = ['lsof', '-i', f'tcp:{host.ssh_port.port_number}']
        with Popen(command, stdout=PIPE) as script:
            #print(script.stdout.read())
            #print(script)

            port_result = f"{script.stdout.read().decode('ascii')}"

            if port_result:
                host.is_online = True
                host.save()
            else:
                host.is_online = False
                host.save()


    return json.dumps({
        'hosts':f'{hosts.values()}',
        'script':f'{command}',
        'Port_Result':f'{port_result}'
    })
