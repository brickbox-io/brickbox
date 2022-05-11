''' Tasks that can be called upon. '''

from __future__ import absolute_import, unicode_literals

from celery import shared_task

import box

from bb_data.models import UserProfile, ResourceTimeTracking
from bb_vm.models import (
    PortTunnel, VirtualBrick, HostFoundation, VirtualBrickOwner
)


# ---------------------------------------------------------------------------- #
#                                Scripted Tasks                                #
# ---------------------------------------------------------------------------- #

# -------------------------------- Shutdown VM ------------------------------- #
@shared_task
def pause_vm_subprocess(instance_id):
    '''
    Called to power down a VM.
    '''
    host = VirtualBrick.objects.get(id=instance_id).host
    virtual_machine = box.Brick(host_port=host.ssh_port, brick_id=f'{str(instance_id)}')
    virtual_machine.toggle_state(set_state="off")


# --------------------------------- Bootup VM -------------------------------- #
@shared_task
def play_vm_subprocess(instance_id):
    '''
    Resume VM from off state.
    '''
    host = VirtualBrick.objects.get(id=instance_id).host
    virtual_machine = box.Brick(host_port=host.ssh_port, brick_id=f'{str(instance_id)}')
    virtual_machine.toggle_state(set_state="on")

# --------------------------------- Reboot VM -------------------------------- #
@shared_task
def reboot_vm_subprocess(instance_id):
    '''
    Called to reboot a VM.
    '''
    host = VirtualBrick.objects.get(id=instance_id).host
    virtual_machine = box.Brick(host_port=host.ssh_port, brick_id=f'{str(instance_id)}')
    virtual_machine.reboot()

# --------------------------------- Delete VM -------------------------------- #
@shared_task
def destroy_vm_subprocess(instance_id, host_id=None):
    '''
    Called to destroy VM.
    '''

    if host_id is None:
        brick = VirtualBrick.objects.get(id=instance_id)
        host = brick.host
    else:
        host = HostFoundation.objects.get(id=host_id)

    virtual_machine = box.Brick(host_port=host.ssh_port, brick_id=f'{str(instance_id)}')
    virtual_machine.destroy()

    if host_id is None:
        brick.delete()

# ---------------------------- Terminate SSH Port ---------------------------- #
@shared_task
def close_ssh_port(port_number):
    '''
    Called when a VM is being destryed, a delay is set before the port becomes available again.
    '''
    PortTunnel.objects.filter(port_number=port_number).delete()

# ------------------------ Destroy VMs With Open Tabs ------------------------ #
@shared_task
def destroy_vm_with_open_tabs(resource_usage_id):
    '''
    Started with a countdown timer when a payment fails.
    If the balance remains unpaid after the timer expires, the VM is destroyed.
    '''
    resource_usage = ResourceTimeTracking.objects.get(id=resource_usage_id)
    user_profile = UserProfile.objects.get(user=resource_usage.user)

    if not resource_usage.balance_paid and not resource_usage.user.is_superuser:
        owned_bricks = VirtualBrickOwner.objects.filter(owner=user_profile)
        for brick in owned_bricks:
            destroy_vm_subprocess.apply_async((brick.virt_brick.id,), queue='ssh_queue')
