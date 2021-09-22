''' CI/CD Functions '''

import subprocess

from django.http import HttpResponse

def pull_update(request):
    '''
    URL: CD/
    Calls script to pull latest changes from github.
    '''
    script_directory = '/opt/brickbox/puller/scripts/'

    with subprocess.Popen([f'{script_directory}continuous_deployment.sh']) as script:
        print(script)


    return HttpResponse(status=200)
