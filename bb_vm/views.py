''' bb_vm views.py '''
# pylint: disable=R0911

import datetime
import subprocess
import urllib.parse

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from bb_data.models import UserProfile, PaymentMethod, CustomScript, ResourceTimeTracking
from bb_vm.models import PortTunnel, VirtualBrick, VirtualBrickOwner, GPU, RentedGPU

from bb_vm.utilities import resource_manager

from bb_tasks.tasks import(
        new_vm_subprocess, destroy_vm_subprocess, close_ssh_port,
        pause_vm_subprocess, play_vm_subprocess, reboot_vm_subprocess,
        stop_bg, host_cleanup, start_bg, attach_gpu_subprocess
    )

DIR = '/opt/brickbox/bb_vm/bash_scripts/'

@login_required()
def clone_img(request):
    '''
    URL: /vm/create/
    Method: AJAX
    Clone exsisting base img to create a new virtual istance.
    '''
    profile = UserProfile.objects.get(user=request.user)
    selected_gpu = request.POST.get('selected_gpu')
    root_pass = request.POST.get('root_pass')
    custom_script = request.POST.get('custom_script')
    if not root_pass:
        root_pass = 'root'
    designated_gpu_xml = None

    cards_available = PaymentMethod.objects.filter(user=profile.user).count()
    rented = VirtualBrickOwner.objects.filter(owner=profile).count()
    response_data = {}

    if not request.user.is_superuser:

        if not profile.brick_access:
            response_data['error'] = 'Account does not have access to bricks.'
            return JsonResponse(response_data, status=200, safe=False)

        if cards_available<1:
            if profile.is_beta and rented >= 2:
                response_data['error'] = "Max Beta VMs Reached"
                return JsonResponse(response_data, status=200, safe=False)

            response_data['error'] = "No payment method provided."
            return JsonResponse(response_data, status=200, safe=False)

        if profile.strikes >= 3:
            response_data['error'] = "Max Strikes Reached"
            return JsonResponse(response_data, status=200, safe=False)

    for gpu in GPU.objects.filter(model=selected_gpu, host__is_ready=True, is_enabled=True):
        if RentedGPU.objects.filter(gpu=gpu).count() < 1:
            designated_gpu_xml = gpu.xml

            instance = VirtualBrick(
                host = gpu.host,
                # name = f'brick-{VirtualBrickOwner.objects.filter(owner=profile).count()+1}'
            )
            instance.save()

            instance.name = f'brick-{instance.id} ({gpu.model})'
            instance.save()

            if custom_script.isdigit():
                instance.user_data = CustomScript.objects.get(id=custom_script)
                instance.save()

            assigned = RentedGPU(gpu=gpu, virt_brick=instance)
            assigned.save()

            brick_owner = VirtualBrickOwner(owner=profile, virt_brick=instance)
            brick_owner.save()

            # Free GPU by shutting down background task
            if gpu.bg_ready:
                stop_bg.apply_async((gpu.id,), queue='ssh_queue')

            new_vm_subprocess.apply_async((instance.id, root_pass,), queue='ssh_queue')

            bricks = VirtualBrickOwner.objects.filter(owner=profile) # All bricks owned.

            response_data['brick_id'] = instance.id
            response_data['table'] = f"""{render_to_string(
                                            'bricks/bricks-instances_table.html',
                                            {'bricks':bricks, 'ssh_url':settings.SSH_URL,}
                                        )}"""

            return JsonResponse(response_data, status=200, safe=False)

    if designated_gpu_xml is None:
        response_data['error'] = f'No available {selected_gpu} GPUs'
        return JsonResponse(response_data, status=200, safe=False)

    return HttpResponse("Error", status=200)


# ------------------------------- Status Update ------------------------------ #
@login_required()
def brick_status(request):
    '''
    URL: /vm/status/
    Method: AJAX
    Returns an update of the users' VMs along with the status of a specific brick.
    '''
    response_data = {}

    profile = UserProfile.objects.get(user = request.user)
    bricks = VirtualBrickOwner.objects.filter(owner=profile) # All bricks owned.

    try:
        brick = VirtualBrick.objects.get(id=request.POST.get("BrickID")) # Brick updating.
        if brick.ssh_port is None:
            response_data['changes'] = False
        else:
            response_data['changes'] = True

    except VirtualBrick.DoesNotExist:
        response_data['changes'] = True

    response_data['table'] = f"""{render_to_string(
                                    'bricks/bricks-instances_table.html',
                                    {'bricks':bricks, 'ssh_url':settings.SSH_URL,}
                                )}"""

    return JsonResponse(response_data, status=200, safe=False)

# ---------------------------------------------------------------------------- #
#                                 Brick Actions                                #
# ---------------------------------------------------------------------------- #

# -------------------------------- Shutdown VM ------------------------------- #
@login_required()
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

    pause_vm_subprocess.apply_async((vm_id,), queue='ssh_queue')

    return HttpResponse(status=200)


# ---------------------------------- Boot VM --------------------------------- #
@login_required()
def brick_play(request):
    '''
    URL:
    Method: AJAX
    Play/Start a paused instance.
    '''
    vm_id = request.POST.get('brick_id')
    profile = UserProfile.objects.get(user=request.user)

     # ------------------------------ Cycyle Balance ------------------------------ #
    tracker, created = ResourceTimeTracking.objects.get_or_create(
                                    user = request.user,
                                    balance_paid = False,
                                    billing_cycle_end__gte=datetime.datetime.today()
                                )
    if created:
        tracker.billing_cycle_end = tracker.billing_cycle_start + datetime.timedelta(days=30)
        tracker.save()

    response_data = {}
    # Prevent starting VM if user has unpaid blance and 3+ strikes.
    if profile.strikes >= 3 and tracker.cycle_total > 0:
        response_data['error'] = "Unpaid balance, update payment method to avoid interuptions."
        return JsonResponse(response_data, status=200, safe=False)

    brick = VirtualBrick.objects.get(id=vm_id)
    brick.is_on = True
    brick.save()

    # Free GPU by shutting down background task
    for rented in RentedGPU.objects.filter(virt_brick=brick):
        if rented.gpu.bg_ready:
            stop_bg.apply_async((rented.gpu.id,), queue='ssh_queue')

    # play_vm_subprocess.delay(vm_id)
    play_vm_subprocess.apply_async((vm_id,), queue='ssh_queue')

    return HttpResponse(status=200)

# --------------------------------- Reboot VM -------------------------------- #
@login_required()
def brick_reboot(request):
    '''
    URL:
    Method: AJAX
    Reboot a instance.
    '''
    vm_id = request.POST.get('brick_id')

    brick = VirtualBrick.objects.get(id=vm_id)
    brick.is_on = True
    brick.is_rebooting = True
    brick.save()

    # reboot_vm_subprocess.delay(vm_id) # Celery Task - Reboot VM
    reboot_vm_subprocess.apply_async((vm_id,), queue='ssh_queue')
    # subprocess.Popen(['/opt/brickbox/bb_vm/bash_scripts/brick_reboot.sh', f'{str(vm_id)}'])

    return HttpResponse(status=200)


# --------------------------------- Remove VM -------------------------------- #
@login_required()
def brick_destroy(request):
    '''
    URL: /vm/brick/destroy/
    Method: AJAX
    Permanently delete a brick instance.
    '''
    vm_id = request.POST.get('brick_id')
    profile = UserProfile.objects.get(user=request.user)

    try:
        brick = VirtualBrick.objects.get(id=vm_id)
        VirtualBrickOwner.objects.filter(virt_brick=brick, owner=profile).delete()

        # Start Port Release Timer
        close_ssh_port.apply_async((brick.ssh_port.port_number,), countdown=43200)

        destroy_vm_subprocess.apply_async((vm_id,), queue='ssh_queue')

        start_bg.apply_async((), queue='ssh_queue')

        pub_key = brick.sshtunnel_public_key
        with subprocess.Popen([f'{DIR}remove_auth_key.sh', f'{str(pub_key)}']) as script:
            print(script)

        profile = UserProfile.objects.get(user = request.user)
        bricks = VirtualBrickOwner.objects.filter(owner=profile) # All bricks owned.
        response_data = {}
        response_data['table'] = f"""{render_to_string(
                                        'bricks/bricks-instances_table.html',
                                        {'bricks':bricks, 'ssh_url':settings.SSH_URL,}
                                    )}"""

    except VirtualBrick.DoesNotExist:
        return HttpResponse("Brick Deleted", status=200)

    return JsonResponse(response_data, status=200, safe=False)


def brick_info(request):
    '''
    URL:/vm/brick/info
    Method: POST
    Returns a summary of the selected brick.
    '''
    brick = VirtualBrick.objects.get(id=request.POST.get('brick_id'))

    brick_data = {}
    brick_data['name'] = brick.name
    brick_data['gpu_count'] = brick.assigned_gpus.count()
    brick_data['cpu_count'] = brick.cpu_count
    brick_data['memory_quantity'] = brick.memory_quantity

    return JsonResponse(brick_data, status=200, safe=False)

def update_brick_resources(request):
    '''
    URL: /vm/brick/update_resources
    Method: POST
    Adds or removes resources from the selected VM.
    '''
    brick = VirtualBrick.objects.get(id=request.POST.get('brick_id'))

    if int(request.POST.get('gpu_count')) > brick.assigned_gpus.count():
        assigned_gpu = resource_manager.get_assigned_gpu(brick.host.id)
        attach_gpu_subprocess.apply_async((brick.id, assigned_gpu.id), queue='ssh_queue')

        assigned_gpu.attached_to = brick
        assigned_gpu.save()

        RentedGPU(
            gpu = assigned_gpu,
            virt_brick = brick,
        ).save()

    return HttpResponse(status=200)


# ---------------------------------------------------------------------------- #
#                           Virtual Machine Endpoints                          #
# ---------------------------------------------------------------------------- #

@csrf_exempt
def vm_tunnel(request):
    '''
    URL: /vm/tunnel/
    Method: POST
    Arguments: pub_key, domain_uuid
    A public SSH key is provided and added to the authorised keys.
    Returns the port number that has been assigned to the VM.
    '''
    try:
        brick = VirtualBrick.objects.get(domain_uuid=request.POST.get('domain_uuid'))
    except VirtualBrick.DoesNotExist:
        host_cleanup.apply_async()
        return HttpResponse(status=400)

    pub_key = urllib.parse.unquote(request.POST.get("pub_key"))

    assigned_port = PortTunnel()
    assigned_port.save()

    brick.ssh_port = assigned_port
    brick.sshtunnel_public_key = pub_key
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
