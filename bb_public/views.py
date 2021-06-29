'''views.py for bb_public'''

from django.shortcuts import render

def landing(request):
    '''
    URL: brickbox.io
    '''
    return render(request, 'landing.html')

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
