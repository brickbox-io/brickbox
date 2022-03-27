''' bb_dashboard - views_tab_developer.py '''

from curses.ascii import HT
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from bb_data.models import CustomScript

@login_required
def add_new_script(request):
    '''
    URL: dashboard/tab/developer/script_add/
    '''
    print(request.POST)
    new_script = CustomScript(
                    user = request.user,
                    name = request.POST.get('script_name'),
                    description = request.POST.get('script_description'),
                    script = request.POST.get('script_code'),
                )
    new_script.save()

    return HttpResponse(status=200)
