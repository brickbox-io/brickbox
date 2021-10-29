''' Tasks that are setup to run continiously in the background. '''

from __future__ import absolute_import, unicode_literals

import json

from subprocess import Popen, PIPE

from django.contrib.sites.models import Site

from celery import shared_task

from bb_vm.models import PortTunnel, HostFoundation, GPU, VirtualBrick

DIR = '/opt/brickbox/bb_vm/bash_scripts/'

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

            port_result = f"{script.stdout.read().decode('ascii')}"

            if port_result and not host.is_online:
                reconnect_host.delay(host.id)

                host.is_online = True
                host.save()
            elif not port_result and host.is_online:
                host.is_online = False
                host.save()

    return json.dumps({
        'hosts':f'{hosts.values()}',
        'script':f'{command}',
        'Port_Result':f'{port_result}'
    })


@shared_task
def verify_brick_connectivity():
    '''
    Checks that virtual machine are connected by cycling through ports to verify activity.
    '''
    bricks = VirtualBrick.objects.all()

    port_result = False
    script = False

    for brick in bricks:
        command = ['lsof', '-i', f'tcp:{brick.ssh_port.port_number}']
        with Popen(command, stdout=PIPE) as script:

            port_result = f"{script.stdout.read().decode('ascii')}"

            if port_result and not brick.is_online:
                PortTunnel.objects.filter(
                    port_number=brick.ssh_port.port_number
                ).update(is_alive=True)
                # brick.ssh_port.is_alive = True
                # brick.save()
            elif not port_result and brick.is_online:
                PortTunnel.objects.filter(
                    port_number=brick.ssh_port.port_number
                ).update(is_alive=False)
                # brick.ssh_port.is_alive = False
                # brick.save()

    return json.dumps({
        'bricks':f'{bricks.values()}',
        'script':f'{command}',
        'Port_Result':f'{port_result}'
    })


# ---------------------------------------------------------------------------- #
#                               Preperation Tasks                              #
# ---------------------------------------------------------------------------- #

@shared_task
def reconnect_host(host):
    '''
    Called whem a host is reconnected.
    '''
    preperation_script = [
                            f'{DIR}brick_connect.sh',
                            'brick_prep',
                            f'{str(Site.objects.get_current().domain)}',
                        ]
    with Popen(preperation_script, stdout=PIPE) as script:
        try:
            prep_script_result = f"{script.stdout.read().decode('ascii')}"
        except AttributeError:
            prep_script_result = 'No output'

    host = HostFoundation.objects.get(id=host)
    for gpu in GPU.objects.filter(host=host):
        reconnect_script = [
                            f'{DIR}brick_connect.sh',
                            'brick_reconnect',
                            f'{str(Site.objects.get_current().domain)}',
                            f'{gpu.device}',
                            f'{gpu.pcie}'
                            ]
        with Popen(reconnect_script) as script:
            try:
                reconnect_script_result = f"{script.stdout.read().decode('ascii')}"
            except AttributeError:
                reconnect_script_result = 'No output'

    return json.dumps({
        'host':f'{host}',
        'PrepScript':f'{preperation_script}',
        'PrepScriptResult':f'{prep_script_result}',
        'ReconnectScript':f'{reconnect_script}',
        'ReconnectScriptResult':f'{reconnect_script_result}',
    })
