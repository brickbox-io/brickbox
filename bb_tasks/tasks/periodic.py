''' Tasks that are setup to run continiously in the background. '''

from __future__ import absolute_import, unicode_literals

from subprocess import Popen, PIPE
import datetime


from django.conf import settings
from django.contrib.sites.models import Site

from celery import shared_task

from bb_vm.models import PortTunnel, HostFoundation, GPU, VirtualBrick, VirtualBrickOwner
from bb_data.models import ResourceTimeTracking

# Script directory on server.
DIR = '/opt/brickbox/bb_vm/bash_scripts/'

@shared_task
def verify_host_connectivity():
    '''
    Checks that hosts are connected by cycling through ports to verify activity.
    '''
    hosts = HostFoundation.objects.all()

    port_result = False
    script = False
    command = False

    for host in hosts:
        command = ['lsof', '-i', f'tcp:{host.ssh_port.port_number}']
        with Popen(command, stdout=PIPE) as script:

            port_result = f"{script.stdout.read().decode('ascii')}"

            # Reconnect if host goes from offline > online
            if port_result and not host.is_online and host.is_enabled:
                reconnect_host.apply_async((host.id,), queue='ssh_queue')
                host.is_online = True
                host.is_ready = False
                host.save()
            elif not port_result and host.is_online:
                host.is_online = False
                host.is_ready = False
                host.save()

    return {
        'hosts':f'{hosts.values()}',
        'script':f'{command}',
        'Port_Result':f'{port_result}'
    }


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
        try:
            if brick.ssh_port.port_number is not None:
                command = ['lsof', '-i', f'tcp:{brick.ssh_port.port_number}']
                with Popen(command, stdout=PIPE) as script:

                    port_result = f"{script.stdout.read().decode('ascii')}"

                    if port_result and not brick.is_online:
                        PortTunnel.objects.filter(
                            port_number=brick.ssh_port.port_number
                        ).update(is_alive=True)

                        VirtualBrick.objects.filter(
                            id=brick.id
                        ).update(is_rebooting=False)
                    elif not port_result and brick.is_online:
                        PortTunnel.objects.filter(
                            port_number=brick.ssh_port.port_number
                        ).update(is_alive=False)
                        # brick.ssh_port.is_alive = False
                        # brick.save()
                    else:
                        VirtualBrick.objects.filter(
                            id=brick.id
                        ).update(is_rebooting=False)
        except AttributeError as err:
            port_result = f"{err}"


    return {
        'bricks':f'{bricks.values()}',
        'script':f'{command}',
        'Port_Result':f'{port_result}'
    }


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
    is_ready = False    # Used to indicate all checks have completed successfully.

    preperation_script = [
                            f'{DIR}brick_connect.sh',
                            f'{str(host.ssh_username)}', f'{str(host.ssh_port)}',
                            'brick_prep', f'{str(Site.objects.get_current().domain)}',
                            'NONE', 'NONE', 'NONE'
                        ]
    if settings.DEBUG:
        preperation_script.insert(1, '-d')

    with Popen(preperation_script, stdout=PIPE) as script:
        try:
            prep_script_result = f"{script.stdout.read().decode('ascii')}"
            prep_script_result_code = script.poll()
            if prep_script_result_code == 0:
                is_ready = True
        except AttributeError:
            prep_script_result = 'No output'
            prep_script_result_code = 'No return code'

    reconnect_script = "No GPUs"
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
                if script.poll() != 0:
                    is_ready = False
            except AttributeError:
                reconnect_script_result = 'No output'

    # Cycle through VM and update power status (Replaced with autostart)
    # for brick_vm in VirtualBrick.objects.filter(host=host):
    #     if brick_vm.is_on:
    #         restore_vm_state.delay(brick_vm.id)


    host.is_ready = is_ready
    host.save()

    return {
        'host':f'{host}',
        'PrepScript':f'{preperation_script}',
        'PrepScriptResult':f'{prep_script_result}',
        'PrepScriptResultCode':f'{prep_script_result_code}',
        'ReconnectScript':f'{reconnect_script}',
        'ReconnectScriptResult':f'{reconnect_script_result}',
    }

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

# ---------------------------------------------------------------------------- #
#                                    Billing                                   #
# ---------------------------------------------------------------------------- #
@shared_task
def resource_time_track():
    '''
    Increments the time a resource is used every minute.
    '''
    bricks = VirtualBrick.objects.all()

    for brick in bricks:
        user = VirtualBrickOwner.objects.get(virt_brick=brick).owner.user
        gpus = brick.assigned_gpus.all()

        for gpu in gpus:
            model = gpu.model

            tracker, created = ResourceTimeTracking.objects.get_or_create(
                                    user = user,
                                    balance_paid = False,
                                    billing_cycle_end__gte=datetime.datetime.today()
                                )

            if created:
                tracker.billing_cycle_end = tracker.billing_cycle_start+datetime.timedelta(days=30)

            setattr(
                tracker, f'minutes_{model}',
                (getattr(tracker, f'minutes_{model}') + 1)
            )

            tracker.save()

@shared_task
def host_cleanup():
    '''
    Ensures tempory issues are resolved.
    '''
    hosts = HostFoundation.objects.all()

    for host in hosts:
        cleanup_script = [
                                f'{DIR}brick_connect.sh',
                                f'{str(host.ssh_username)}', f'{str(host.ssh_port)}',
                                'host_cleanup', f'{str(Site.objects.get_current().domain)}',
                                f'{str(host.id)}', 'NONE', 'NONE'
                            ]

        with Popen(cleanup_script) as script:
            print(script)

    return {
        'hosts':f'{hosts.values()}',
    }
