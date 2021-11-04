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

            # Reconnect if host goes from offline > online
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
    command = "No Command Ran"

    for brick in bricks:
        if brick.ssh_port.port_number is not None:
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
    GPU - Cycles through all GPUs and changes driver to VFIO.
    VM - Cycles through all VMs and updates their power status.
    '''
    host = HostFoundation.objects.get(id=host)

    preperation_script = [
                            f'{DIR}brick_connect.sh',
                            f'{str(host.ssh_username)}', f'{str(host.ssh_port)}',
                            'brick_prep', f'{str(Site.objects.get_current().domain)}',
                        ]

    with Popen(preperation_script, stdout=PIPE) as script:
        try:
            prep_script_result = f"{script.stdout.read().decode('ascii')}"
        except AttributeError:
            prep_script_result = 'No output'

    reconnect_script = "Not GPUs"
    reconnect_script_result = "Not Ran"

    for gpu in GPU.objects.filter(host=host):
        reconnect_script = [
                                f'{DIR}brick_connect.sh',
                                f'{str(host.ssh_username)}', f'{str(host.ssh_port)}',
                                'brick_reconnect', f'{str(Site.objects.get_current().domain)}',
                                f'{gpu.device}',
                                f'{gpu.pcie}'
                            ]

        with Popen(reconnect_script) as script:
            try:
                reconnect_script_result = f"{script.stdout.read().decode('ascii')}"
            except AttributeError:
                reconnect_script_result = 'No output'

    # Cycle through VM and update power status
    for brick_vm in VirtualBrick.objects.filter(host=host):
        if brick_vm.is_on:
            restore_vm_state.delay(brick_vm.id)


    return json.dumps({
        'host':f'{host}',
        'PrepScript':f'{preperation_script}',
        'PrepScriptResult':f'{prep_script_result}',
        'ReconnectScript':f'{reconnect_script}',
        'ReconnectScriptResult':f'{reconnect_script_result}',
    })

@shared_task
def restore_vm_state(instance):
    '''
    Called to restore the powered state of the VM.
    '''
    host = VirtualBrick.objects.get(id=instance).host

    play_vm_script = [
                        f'{DIR}brick_connect.sh',
                        f'{str(host.ssh_username)}', f'{str(host.ssh_port)}',
                        'brick_play', f'{str(Site.objects.get_current().domain)}',
                        f'{str(instance)}'
                    ]

    with Popen(play_vm_script) as script:
        print(script)
