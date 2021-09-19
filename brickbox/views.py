''' Base level functionality. '''

import subprocess

from django.http import HttpResponse

def pull_update(request):
    '''
    URL: CD/
    Calls script to pull latest changes from github.
    '''
    DIR = '/opt/brickbox/brickbox/scripts/'

    with subprocess.Popen([f'{DIR}continuous_deployment.sh']) as script:
        print(script)


    return HttpResponse(status=200)
