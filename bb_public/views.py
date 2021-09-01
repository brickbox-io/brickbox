'''views.py for bb_public'''

from django.shortcuts import render

def landing_ai(request):
    '''
    URL: brickbox.io
    '''
    return render(request, 'landing_ai.html')

def about(request):
    '''
    URL: brickbox.io/about
    '''
    return render(request, 'about.html')

def contact(request):
    '''
    URL: brickbox.io/contact
    '''
    return render(request, 'contact.html')

def landing_colo(request):
    '''
    URL: brickbox.io/colo
    '''
    return render(request, 'landing_colo.html')
