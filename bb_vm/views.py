''' bb_vm views.py '''

import subprocess
import urllib.parse

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from bb_data.models import UserProfile
from bb_vm.models import PortTunnel, VirtualBrick, VirtualBrickOwner, GPU, RentedGPU

from bb_tasks.tasks import(
        new_vm_subprocess, destroy_vm_subprocess, close_ssh_port,
        pause_vm_subprocess, play_vm_subprocess, reboot_vm_subprocess,
    )

DIR = '/opt/brickbox/bb_vm/bash_scripts/'

@csrf_exempt
@login_required(login_url="/login/")
def clone_img(request):
    '''
    URL: /vm/create/
    Method: AJAX
    Clone exsisting image to create a new istance.
    '''
    designated_gpu_xml = None
    for gpu in GPU.objects.all():
        if RentedGPU.objects.filter(gpu=gpu).count() < 1:
            designated_gpu_xml = gpu.xml

            profile = UserProfile.objects.get(user=request.user)

            instance = VirtualBrick(
                name=f'brick-{VirtualBrickOwner.objects.filter(owner=profile).count()+1}'
            )
            instance.save()

            assigned = RentedGPU(gpu=gpu, virt_brick=instance)
            assigned.save()

            brick_owner = VirtualBrickOwner(owner=profile, virt_brick=instance)
            brick_owner.save()

            new_vm_subprocess.delay(instance.id, designated_gpu_xml)

            # subprocess.Popen([
            #     '/opt/brickbox/bb_vm/bash_scripts/clone_img.sh',
            #     f'{str(instance.id)}', f'{str(designated_gpu_xml)}'
            # ])

            bricks = VirtualBrickOwner.objects.filter(owner=profile) # All bricks owned.
            response_data = {}
            response_data['brick_id'] = instance.id
            response_data['table'] = f"""{render_to_string(
                                            'bricks/bricks-instances_table.html',
                                            {'bricks':bricks, 'ssh_url':settings.SSH_URL,}
                                        )}"""

            return JsonResponse(response_data, status=200, safe=False)

    if designated_gpu_xml is None:
        return HttpResponse("No Available GPUs", status=200)

    return HttpResponse("Error", status=200)

# ------------------------------- Status Update ------------------------------ #
@csrf_exempt
@login_required(login_url="/login/")
def brick_status(request):
    '''
    URL: /vm/status/
    Method: AJAX
    Returns an update of the users' VMs along with the status of a specific brick.
    '''
    profile = UserProfile.objects.get(user = request.user)
    bricks = VirtualBrickOwner.objects.filter(owner=profile) # All bricks owned.
    brick = VirtualBrick.objects.get(id=request.POST.get("BrickID")) # Brick updating.

    response_data = {}

    if brick.ssh_port is None:
        response_data['changes'] = False
    else:
        response_data['changes'] = True
    response_data['table'] = f"""{render_to_string(
                                    'bricks/bricks-instances_table.html',
                                    {'bricks':bricks, 'ssh_url':settings.SSH_URL,}
                                )}"""

    return JsonResponse(response_data, status=200, safe=False)


# -------------------------------- Shutdown VM ------------------------------- #
@csrf_exempt
@login_required(login_url="/login/")
def brick_pause(request):
    '''
    URL:
    Method: AJAX
    Pauses an instance that can resumed later.
    '''
    vm_id = request.POST.get('brick_id')

    brick = VirtualBrick.objects.get(id=vm_id)
    brick.is_on = False
    brick.save()

    pause_vm_subprocess.delay(vm_id)
    # subprocess.Popen(['/opt/brickbox/bb_vm/bash_scripts/brick_pause.sh', f'{str(vm_id)}'])

    return HttpResponse(status=200)


# ---------------------------------- Boot VM --------------------------------- #
@csrf_exempt
@login_required(login_url="/login/")
def brick_play(request):
    '''
    URL:
    Method: AJAX
    Play/Start a paused instance.
    '''
    vm_id = request.POST.get('brick_id')

    brick = VirtualBrick.objects.get(id=vm_id)
    brick.is_on = True
    brick.save()

    play_vm_subprocess.delay(vm_id)
    # subprocess.Popen(['/opt/brickbox/bb_vm/bash_scripts/brick_play.sh', f'{str(vm_id)}'])

    return HttpResponse(status=200)

# --------------------------------- Reboot VM -------------------------------- #
@csrf_exempt
@login_required(login_url="/login/")
def brick_reboot(request):
    '''
    URL:
    Method: AJAX
    Reboot a instance.
    '''
    vm_id = request.POST.get('brick_id')

    brick = VirtualBrick.objects.get(id=vm_id)
    brick.is_on = True
    brick.save()

    reboot_vm_subprocess.delay(vm_id)
    # subprocess.Popen(['/opt/brickbox/bb_vm/bash_scripts/brick_reboot.sh', f'{str(vm_id)}'])

    return HttpResponse(status=200)


# --------------------------------- Remove VM -------------------------------- #
@csrf_exempt
@login_required(login_url="/login/")
def brick_destroy(request):
    '''
    URL: /vm/brick/destroy/
    Method: AJAX
    Permanently delete a brick instance.
    '''
    vm_id = request.POST.get('brick_id')

    brick = VirtualBrick.objects.get(id=vm_id)
    VirtualBrickOwner.objects.filter(virt_brick=brick).delete()
    brick.delete()
    # brick.ssh_port.delete()
    close_ssh_port.apply_async((brick.ssh_port.port_number,), countdown=43200)

    destroy_vm_subprocess.delay(vm_id)

    # subprocess.Popen(['/opt/brickbox/bb_vm/bash_scripts/brick_destroy.sh', f'{str(vm_id)}'])

    profile = UserProfile.objects.get(user = request.user)
    bricks = VirtualBrickOwner.objects.filter(owner=profile) # All bricks owned.
    response_data = {}
    response_data['table'] = f"""{render_to_string(
                                    'bricks/bricks-instances_table.html',
                                    {'bricks':bricks, 'ssh_url':settings.SSH_URL,}
                                )}"""

    return JsonResponse(response_data, status=200, safe=False)


# ---------------------------------------------------------------------------- #
#                           Virtual Machine Endpoints                          #
# ---------------------------------------------------------------------------- #

@csrf_exempt
def vm_tunnel(request):
    '''
    URL: /vm/tunnel/
    Method: POST
    A public SSH key is provided and added to the authorised keys.
    Returns the port number that has been assigned to the VM.
    '''
    # print(request.POST.get("pub_key"))
    # print(request.POST.get('domain_uuid'))

    pub_key = urllib.parse.unquote(request.POST.get("pub_key"))
    # print(pub_key)
    assigned_port = PortTunnel()
    assigned_port.save()

    brick = VirtualBrick.objects.get(domain_uuid=request.POST.get('domain_uuid'))
    brick.ssh_port = assigned_port
    brick.is_on = True
    brick.save()

    with subprocess.Popen([f'{DIR}auth_key.sh', f'{str(pub_key)}']) as script:
        print(script)

    return HttpResponse(brick.ssh_port.port_number, status=200)


def vm_register(request, instance_id, domain_uuid):
    '''
    URL: /vm/register/<instance_id>/<domain_id>/
    Method: GET
    Links an exsisting instance to the VM UUID.
    '''
    instance = VirtualBrick.objects.get(id=instance_id)
    instance.domain_uuid = domain_uuid
    instance.save()

    return HttpResponse(status=200)
