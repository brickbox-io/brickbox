'''views.py for bb_dashboard'''

from django.shortcuts import render

from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def dashboard(request):
    '''
    URL: /dash/
    Method: GET
    Returns the main dash board where a user can see statisics and or create bricks.
    '''
    return render(request, 'dashboard.html')
