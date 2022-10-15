''' bb_vm - models_hosts.py '''

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete

import box

from bb_data.models import ColocationClient

# ----------------------------------- Hosts ---------------------------------- #
class HostFoundation(models.Model):
    '''
    Represents the host computer/server where the virtual machines will reside.
    Recivers(s): assign_host_ssh_port
    '''
    vpn_ip = models.GenericIPAddressField(unique=True, null=True, blank=True) # OpenVPN IP
    serial_number = models.CharField(max_length=64, null=True, unique=True)  # Host serial number

    # SSH Tunnel
    ssh_port = models.ForeignKey(
                    'bb_vm.PortTunnel', blank=True, null=True, on_delete=models.PROTECT)

    sshtunnel_public_key = models.TextField(blank=True, null=True)  # Key to establish SSH tunnel

    # Root User
    ssh_username = models.CharField(max_length = 64, default="bb_root")

    # Available Resources
    cpu_cores = models.IntegerField(default=12) # Real Cores
    memory = models.IntegerField(default=12)    # GB

    # Flags
    is_enabled = models.BooleanField(default=False)      # Enabled/Disabled for use
    is_online = models.BooleanField(default=False)      # Online if tunnel is alive
    is_ready = models.BooleanField(default=False)       # All checks passed

    def __str__(self):
        if self.vpn_ip:
            return f"{self.vpn_ip}"
        return f"{self.serial_number}"

    class Meta:
        verbose_name_plural = "A - Hosts"

# --------------------------- Host Port Allocation --------------------------- #
@receiver(pre_save, sender=HostFoundation)
def assign_host_ssh_port(sender, instance, **kwargs):
    '''
    Assigns first available port number to new SSH instance.
    '''
    print(sender)

    # Host Ready Status
    if not instance.is_online:
        instance.is_ready = False

    if instance.ssh_port is None:
        assigned_port = PortTunnel()
        assigned_port.save()
        instance.ssh_port = assigned_port
        instance.save()

# ------------------------------ Equipment Owner ----------------------------- #
class EquipmentOwner(models.Model):
    '''
    Pairs equipment with a colo client account.
    '''
    client_account = models.ForeignKey(ColocationClient, on_delete=models.PROTECT)
    server = models.ForeignKey('HostFoundation', on_delete=models.PROTECT)
    date_ordered = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "K - Equipment Owners"

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

    class Meta:
        verbose_name_plural = "G - Tunnel Ports"

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

# ----------------------------------- GPUs ----------------------------------- #
class GPU(models.Model):
    '''
    Stores all GPUs available.
    '''
    host = models.ForeignKey(HostFoundation, on_delete=models.PROTECT) # The physical host.
    model = models.CharField(max_length = 36) # i.e. 1080, 3090

    is_enabled = models.BooleanField(default=True) # Enabled/Disabled for use

    pcie = models.CharField(max_length = 64) # Domain:Bus:Device.Function - dddd:vv:dd.f
    device = models.CharField(max_length = 32) # Vendor:Device - vvvv:dddd

    xml = models.TextField(null=True)

    rented = models.BooleanField(default = False)
    attached_to = models.ForeignKey('VirtualBrick', null=True, blank=True, on_delete=models.SET_NULL)

    # Background Tasks
    bg_ready = models.BooleanField(default = False) # Indicates that an img is ready for the GPU
    bg_running = models.BooleanField(default = False) # Background task running

    class Meta:
        verbose_name_plural = "B - GPUs"

@receiver(pre_save, sender=GPU)
def toggle_bg_task(sender, instance, **kwargs):
    '''
    Toggles background task before saving.
    '''
    print(sender)
    if not instance.host.is_online:
        return

    if instance.rented and instance.bg_ready:
        box.Brick(
            host_port = instance.host.ssh_port,
            brick_id = f'gpu_{str(instance.id)}'
        ).toggle_state(set_state="off")
        instance.bg_running = False

    elif not instance.rented and instance.bg_ready:
        box.Brick(
            host_port = instance.host.ssh_port,
            brick_id = f'gpu_{str(instance.id)}'
        ).toggle_state(set_state="on")
        instance.bg_running = True

    return

# -------------------------------- Rented GPUs ------------------------------- #
class RentedGPU(models.Model):
    '''
    Allocates a GPU to a virtual machine.
    Reciver(s): update_rent_status, update_rent_status_available
    '''
    gpu = models.OneToOneField('GPU', on_delete=models.PROTECT, null=True)
    virt_brick = models.ForeignKey('VirtualBrick', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name_plural = "D - Rented GPUs"

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
