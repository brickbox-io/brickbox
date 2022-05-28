''' bb_vm - models_vms.py'''

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import  post_save

from django.utils.translation import gettext_lazy as _

from bb_data.models import UserProfile


# ----------------------------- Virtual Machines ----------------------------- #
class VirtualBrick(models.Model):
    '''
    Represents a single VM instance.
    Recivers(s): update_vm_history,
    '''
    # Physical host.
    host = models.ForeignKey('bb_vm.HostFoundation', on_delete=models.PROTECT, null=True)

    name = models.CharField(max_length = 36, null=True)         # Arbitrary Name
    domain_uuid = models.UUIDField(max_length = 36, null=True)  # UUID of the VM (serial="domain")
    ssh_port = models.ForeignKey('bb_vm.PortTunnel', on_delete=models.PROTECT, null=True)
    sshtunnel_public_key = models.TextField(blank=True, null=True)  # Key to establish SSH tunnel

    # Cloud-init
    user_data = models.ForeignKey(
                    'bb_data.CustomScript',
                    on_delete=models.RESTRICT,
                    null=True, blank=True
                )

    owners = models.ManyToManyField(
                    UserProfile,
                    through='VirtualBrickOwner',
                    related_name='brick_owner'
                )

    # Resources
    assigned_gpus = models.ManyToManyField('GPU', through='RentedGPU', related_name='assigned_gpus')
    cpu_count = models.IntegerField(default=4)
    memory_quantity = models.IntegerField(default=12) # in GB

    img_cloned = models.BooleanField(default = False) # True when img clone verified
    is_booting = models.BooleanField(default = True) # True when VM is booting
    is_rebooting = models.BooleanField(default = False)
    is_on = models.BooleanField(default = False) # True when VM is running

    @property
    def is_online(self):
        '''
        Returns True if the VM is accessible via SSH port.
        '''
        return self.ssh_port.is_alive

    class Meta:
        verbose_name_plural = "C - Virtual Machines (Bricks)"

# ------------------------------- Brick Hstory ------------------------------- #
@receiver(post_save, sender=VirtualBrick)
def update_vm_history(sender, instance, created, **kwargs):
    '''
    Updates the history of the virtual brick.
    '''
    print(sender)
    if created:
        history = VirtualBrickHistory()
        history.brick = instance.id
        history.save()


# --------------------------------- VM Owners -------------------------------- #
class VirtualBrickOwner(models.Model):
    '''
    Pairs a virtual brick to a user.
    Recivers(s): update_vm_woner_history
    '''
    owner = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    virt_brick = models.ForeignKey(VirtualBrick, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "J - VM Owners"

@receiver(post_save, sender=VirtualBrickOwner)
def update_vm_owner_history(sender, instance, created, **kwargs):
    '''
    Updates the history of the virtual brick.
    '''
    print(sender)
    if created:
        VirtualBrickHistory.objects.filter(brick=instance.virt_brick.id).update(
            creator=instance.owner
        )

# ----------------------------- VM History (Log) ----------------------------- #
class VirtualBrickHistory(models.Model):
    '''
    Contains history of a virtual brick.
    '''
    brick = models.CharField(max_length=32)
    creator = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)

    date_destroyed = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "H - VM History"


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
        verbose_name_plural = "I - VM Logs"
