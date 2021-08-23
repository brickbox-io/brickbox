''' Models for bb_vm '''

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save

from bb_data.models import UserProfile

class PortTunnel(models.Model):
    '''
    Acts as a lookup table for available ports that can be assigned for SSH access.
    '''
    port_number = models.IntegerField(unique=True)

@receiver(pre_save, sender=PortTunnel)
def assign_port(sender, instance, **kwargs):
    '''
    Assigned first available port number to new SSH instance.
    '''
    print(sender)
    if instance.port_number is None:
        for port in range(1025, 65535):
            if PortTunnel.objects.filter(port_number=port).count() < 1:
                instance.port_number = port
                instance.save()

                break


class HostFoundation(models.Model):
    '''
    Represents the host computer/server where the virtual machines will reside.
    '''
    ssh_port = models.ForeignKey(PortTunnel, on_delete=models.PROTECT)
    ssh_username = models.CharField(max_length = 64)


class GPU(models.Model):
    '''
    Stores all GPUs available.
    '''
    host = models.ForeignKey(HostFoundation, on_delete=models.PROTECT) # The physical host.
    model = models.CharField(max_length = 36) # i.e. 1080, 3090

    pcie = models.CharField(max_length = 64) # Domain:Bus:Device.Function - dddd:vv:dd.f
    device = models.CharField(max_length = 32) # Vendor:Device - vvvv:dddd

    xml = models.TextField(null=True)

class RentedGPU(models.Model):
    '''
    Allocates a GPU to a virtual machine.
    '''
    gpu = models.ForeignKey('GPU', on_delete=models.PROTECT, null=True)
    virt_brick = models.ForeignKey('VirtualBrick', on_delete=models.CASCADE, blank=True, null=True)


class VirtualBrick(models.Model):
    '''
    Represents a single VM instance.
    '''
    name = models.CharField(max_length = 36, null=True) # Arbitrary Name
    domain_uuid = models.CharField(max_length = 36, null=True) # UUID of the VM
    assigned_gpus = models.ManyToManyField('GPU', through='RentedGPU', related_name='assigned_gpus')
    ssh_port = models.ForeignKey(PortTunnel, on_delete=models.PROTECT, null=True)

    owners = models.ManyToManyField(
                    UserProfile,
                    through='VirtualBrickOwner',
                    related_name='brick_owner'
                )

    is_on = models.BooleanField(default = False)


class VirtualBrickOwner(models.Model):
    '''
    Pairs a virtual brick to a user.
    '''
    owner = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    virt_brick = models.ForeignKey(VirtualBrick, on_delete=models.PROTECT)