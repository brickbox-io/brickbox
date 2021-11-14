'''
bb_vm views for hosts
- Onboarding
'''

import subprocess
import urllib.parse

from django.http import HttpResponse
# from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from bb_vm.models import HostFoundation, GPU

DIR = '/opt/brickbox/bb_vm/bash_scripts/'

@csrf_exempt
# @login_required
def onboarding(request, host_serial):
    '''
    Starting point for onboarding new hosts.
    URL: brickbox.io/vm/host/onboarding
    Method: POST
    Submit serial number and Publick Key, await 200 response to proceed.
    '''
    if request.method == 'POST':
        print(request.POST)

        public_key = urllib.parse.unquote(request.POST.get("public_key"))

        if host_serial and public_key:
            try:
                host = HostFoundation.objects.get(serial_number=host_serial)
                host.sshtunnel_public_key = public_key
                host.save()

                with subprocess.Popen([f'{DIR}auth_key.sh', f'{str(public_key)}']) as script:
                    print(script)

                return HttpResponse("ok", status=200)
            except HostFoundation.DoesNotExist:
                return HttpResponse("error", status=404)

        return HttpResponse("error", status=400)

    return HttpResponse("error", status=405)


@csrf_exempt
# @login_required
def onboarding_pubkey(request, host_serial):
    '''
    Endpoint for onboarding a host.
    URL: brickbox.io/vm/host/onboarding/pubkey
    Method: POST
    Make a request to recive the public key for the root user.
    '''
    if request.method == 'POST':
        print(request.POST)

        if host_serial:
            try:
                HostFoundation.objects.get(serial_number=host_serial)
                with open("/opt/brickbox/bb_vm/keys/bb_root.pub", encoding="utf-8") as pubkey_file:
                    pubkey = pubkey_file.read()

                return HttpResponse(pubkey, status=200)

            except HostFoundation.DoesNotExist:
                return HttpResponse("error", status=404)

        return HttpResponse("error", status=400)

    return HttpResponse("error", status=405)


@csrf_exempt
# @login_required
def onboarding_sshport(request, host_serial):
    '''
    Endpoint for the process of onboarding a new host.
    URL: brickbox.io/vm/host/onboarding/sshport
    Method: POST
    Make a request to recive the assigned SSH tunnel port.
    '''
    if request.method == 'POST':
        print(request.POST)

        if host_serial:
            try:
                host = HostFoundation.objects.get(serial_number=host_serial)
                return HttpResponse(host.ssh_port, status=200)
            except HostFoundation.DoesNotExist:
                return HttpResponse("error", status=404)

        return HttpResponse("error", status=404)

    return HttpResponse("error", status=405)


@csrf_exempt
def onboarding_gpu(request, host_serial):
    '''
    Endpoint for the process of onboarding a new host.
    URL: brickbox.io/vm/host/onboarding/gpu_registration
    Method: POST
    Make a request to recive the assigned GPU port.
    '''
    if request.method == 'POST':
        print(request.POST)

        if host_serial:
            try:
                host = HostFoundation.objects.get(serial_number=host_serial)

                gpu_model = request.POST.get("gpu_model")
                gpu_device = request.POST.get("gpu_device")

                gpu_pcie = request.POST.get("gpu_pcie")
                bus = gpu_pcie.split(':')[0]

                gpu_pcie = f'0000:{gpu_pcie}'

                # gpu_qty = request.POST.get("gpu_qty")

                new_gpu = GPU(
                                host=host, model=gpu_model,
                                pcie=gpu_pcie, device=gpu_device
                            )

                with open("/opt/brickbox/bb_vm/xml/gpu.xml", encoding="utf-8") as gpu_xml:
                    gpu_xml = gpu_xml.read()
                    new_gpu.xml = gpu_xml.format(bus=bus)
                    new_gpu.save()

                return HttpResponse("ok", status=200)
            except HostFoundation.DoesNotExist:
                return HttpResponse("error", status=404)

        return HttpResponse("error", status=404)

    return HttpResponse("error", status=405)
