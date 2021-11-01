'''views.py for bb_public'''

from django.shortcuts import render, redirect
from django.http import HttpResponse

from bb_public.models import EmailUpdateList

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

# ---------------------------------------------------------------------------- #
#                                     Forms                                    #
# ---------------------------------------------------------------------------- #

def forms_email_list(request):
    '''
    URL: brickbox.io/forms/email_list/
    '''
    print(request.POST)

    new_email = EmailUpdateList(
        email=request.POST['email']
    )
    new_email.save()

    # return redirect('/')
    return HttpResponse('Email Submitted, Thank You', status=200)

# ---------------------------------------------------------------------------- #
#                                      PWA                                     #
# ---------------------------------------------------------------------------- #

# ---------------------------------- Offline --------------------------------- #
def pwa_offline(request):
    '''
    URL: brickbox.io/offline/
    '''
    return render(request, 'pwa_offline.html')
