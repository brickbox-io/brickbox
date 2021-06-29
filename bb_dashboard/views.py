'''views.py for bb_dashboard'''

from django.shortcuts import render

def dashboard(request):
    '''
    URL:
    '''
    return render(request, 'dashboard.html')
