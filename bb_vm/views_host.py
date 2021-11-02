'''
bb_vm views for hosts
- Onboarding
'''

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from bb_vm.models import HostFoundation


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
        public_key = request.POST.get('public_key')

        if host_serial and public_key:
            try:
                host = HostFoundation.objects.get(serial_number=host_serial)
                host.sshtunnel_public_key = public_key
                host.save()
                return HttpResponse('200')
            except HostFoundation.DoesNotExist:
                return HttpResponse('404')

        return HttpResponse(status=200)

    return HttpResponse(status=405)


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
                host = HostFoundation.objects.get(serial_number=host_serial)
                return HttpResponse(host.sshtunnel_public_key)
            except HostFoundation.DoesNotExist:
                return HttpResponse('404')

        return HttpResponse(status=200)


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
                return HttpResponse(host.ssh_port)
            except HostFoundation.DoesNotExist:
                return HttpResponse('404')

        return HttpResponse(status=200)
