''' Functions to handle brick erros as part of closed loop validation. '''

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from bb_vm.models import VirtualBrick

@csrf_exempt
def brick_errors(request):
    '''
    URL: /vm/errors/
    Method: POST
    Used to report an instance id and related error.
    '''
    print(request.POST)

    return HttpResponse(status=200)
