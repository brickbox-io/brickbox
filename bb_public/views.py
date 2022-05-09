'''views.py for bb_public'''

from django.shortcuts import render
from django.http import HttpResponse

from bb_public.models import EmailUpdateList

# ------------------------------- Landing Page ------------------------------- #
def landing_page(request):
    '''
    URL: brickbox.io
    '''
    return render(request, 'landing.html')

# -------------------------------- Legal Page -------------------------------- #
def legal_page(request):
    '''
    URL: brickbox.io/legal
    '''
    return render(request, 'privacy_policy.html')

# ---------------------------------------------------------------------------- #
#                                     Forms                                    #
# ---------------------------------------------------------------------------- #

def email_list_form(request):
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
