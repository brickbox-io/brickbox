''' Models for bb_vm '''

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete

from django.utils.translation import gettext_lazy as _

from bb_data.models import UserProfile


# ----------------------------------- Ports ---------------------------------- #
class PortTunnel(models.Model):
    '''
    Acts as a lookup table for available ports that can be assigned for SSH access.
    Recivers(s): assign_port
    '''
    port_number = models.IntegerField(unique=True)
    is_alive = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.port_number}"


# ----------------------------------- Hosts ---------------------------------- #
class HostFoundation(models.Model):
    '''
    Represents the host computer/server where the virtual machines will reside.
    '''
    serial_number = models.CharField(max_length=64, null=True)  # Uniquely identities a host.

    ssh_port = models.ForeignKey(PortTunnel, on_delete=models.PROTECT)
    ssh_username = models.CharField(max_length = 64)

    active = models.BooleanField(default=True)

    is_online = models.BooleanField(default=False)
    gpus_online = models.BooleanField(default=False)

    connected_status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Host Foundations/Servers"


# ----------------------------------- GPUs ----------------------------------- #
class GPU(models.Model):
    '''
    Stores all GPUs available.
    '''
    host = models.ForeignKey(HostFoundation, on_delete=models.PROTECT) # The physical host.
    model = models.CharField(max_length = 36) # i.e. 1080, 3090

    pcie = models.CharField(max_length = 64) # Domain:Bus:Device.Function - dddd:vv:dd.f
    device = models.CharField(max_length = 32) # Vendor:Device - vvvv:dddd

    xml = models.TextField(null=True)

    rented = models.BooleanField(default = False)

    class Meta:
        verbose_name_plural = "GPUs"


# -------------------------------- Rented GPUs ------------------------------- #
class RentedGPU(models.Model):
    '''
    Allocates a GPU to a virtual machine.
    Reciver(s): update_rent_status, update_rent_status_available
    '''
    gpu = models.ForeignKey('GPU', on_delete=models.PROTECT, null=True)
    virt_brick = models.ForeignKey('VirtualBrick', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Rented GPUs"


# ----------------------------- Virtual Machines ----------------------------- #
class VirtualBrick(models.Model):
    '''
    Represents a single VM instance.
    '''
    host = models.ForeignKey(HostFoundation, on_delete=models.PROTECT, null=True)  # Physical host.
    name = models.CharField(max_length = 36, null=True)         # Arbitrary Name
    domain_uuid = models.UUIDField(max_length = 36, null=True)  # UUID of the VM (serial="domain")
    assigned_gpus = models.ManyToManyField('GPU', through='RentedGPU', related_name='assigned_gpus')
    ssh_port = models.ForeignKey(PortTunnel, on_delete=models.PROTECT, null=True)

    owners = models.ManyToManyField(
                    UserProfile,
                    through='VirtualBrickOwner',
                    related_name='brick_owner'
                )

    img_cloned = models.BooleanField(default = False) # True when img clone verified
    is_rebooting = models.BooleanField(default = False)
    is_on = models.BooleanField(default = False)

    @property
    def is_online(self):
        '''
        Returns True if the VM is connected to the host.
        '''
        return self.ssh_port.is_alive

    class Meta:
        verbose_name_plural = "Virtual Bricks/Machines"


# --------------------------------- VM Owners -------------------------------- #
class VirtualBrickOwner(models.Model):
    '''
    Pairs a virtual brick to a user.
    '''
    owner = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    virt_brick = models.ForeignKey(VirtualBrick, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "VM Owners"


# ---------------------------------- Logging --------------------------------- #
class VMLog(models.Model):
    '''
    Model to store logs relating the VMs.
    '''
    class LogLevels(models.IntegerChoices):
        '''Logging level options'''
        CRITICAL = 50, _('CRITICAL')
        ERROR = 40, _('ERROR')
        WARNING = 30, _('WARNING')
        INFO = 20, _('INFO')
        DEBUG = 10, _('DEBUG')
        NOTSET = 0, _('NOTSET')
        __empty__ = _('NOTSET')

    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.IntegerField(choices=LogLevels.choices)
    host = models.CharField(max_length=32, null=True)
    virt_brick = models.CharField(max_length=32)
    message = models.TextField()

    command = models.TextField(null=True)           # Command that was executed
    command_output = models.TextField(null=True)    # Output of the command

    class Meta:
        verbose_name_plural = "VM Logs"


# ---------------------------------------------------------------------------- #
#                             Recivers and Actions                             #
# ---------------------------------------------------------------------------- #

# ------------------------------ Port Allocation ----------------------------- #
@receiver(pre_save, sender=PortTunnel)
def assign_port(sender, instance, **kwargs):
    '''
    Assigns first available port number to new SSH instance.
    '''
    print(sender)
    if instance.port_number is None:
        for port in range(1025, 65535):
            if PortTunnel.objects.filter(port_number=port).count() < 1:
                instance.port_number = port
                instance.save()

                break

# ----------------------------- GPU Rented Status ---------------------------- #
@receiver(post_save, sender=RentedGPU)
def update_rent_status(sender, instance, created, **kwargs):
    '''
    Updates the rented boolean field of the GPU to True.
    '''
    print(sender)
    if created:
        selected_gpu = instance.gpu
        selected_gpu.rented = True
        selected_gpu.save()

@receiver(post_delete, sender=RentedGPU)
def update_rent_status_available(sender, instance, **kwargs):
    '''
    Updates the rented boolean field of the GPU to False.
    '''
    print(sender)
    selected_gpu = instance.gpu
    selected_gpu.rented = False
    selected_gpu.save()
