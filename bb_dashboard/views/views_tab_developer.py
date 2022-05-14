''' bb_dashboard - views_tab_developer.py '''

from django.http import HttpResponse, JsonResponse
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

@login_required
def edit_script(request, script_id):
    '''
    URL: dashboard/tab/developer/script_edit/<int:script_id>/
    Method: GET
    Returns the script values to be edited
    '''
    script = CustomScript.objects.get(id=script_id)
    return JsonResponse(
        {
            'script_name': script.name,
            'script_description': script.description,
            'script_code': script.script
        }, status=200, safe=False)

@login_required
def update_script(request):
    '''
    URL: dashboard/tab/developer/script_update
    Updates the script changes.
    '''
    script_id = request.POST.get('script_id')

    script = CustomScript.objects.get(id=script_id)

    if script.user != request.user:
        return HttpResponse("Unable to edit selected script", status=403)

    script.name = request.POST.get('script_name')
    script.description = request.POST.get('script_description')
    script.script = request.POST.get('script_code')
    script.save()

    return HttpResponse(status=200)

@login_required
def delete_script(request):
    '''
    URL: dashboard/tab/developer/script_delete
    Method: POST
    Deletes the script.
    '''
    script_id = request.POST.get('script_id')

    script = CustomScript.objects.get(id=script_id)

    if script.user != request.user:
        return HttpResponse("Unable to delete selected script", status=403)

    script.delete()

    return HttpResponse(status=200)
