''' Manages the availability of resources. '''

from faulthandler import is_enabled
from bb_vm.models import HostFoundation, GPU

def available_gpus(host_id=None):
    '''
    Returns a list of available GPUs.
    '''
    host = HostFoundation.objects.get(id=host_id)
    gpus = GPU.objects.filter(host=host, rented=False, is_enabled=True)

    return gpus

def get_assigned_gpu(host_id):
    '''
    Assigns a GPU to a virtual machine.
    '''
    host = HostFoundation.objects.get(id=host_id)
    gpus = GPU.objects.filter(host=host, rented=False, is_enabled=True)

    for gpu in gpus:
        gpu.rented = True
        gpu.save()
        return gpu
