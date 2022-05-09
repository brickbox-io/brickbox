'''views.py for bb_public'''

import email
from email import message
from hashlib import new
from unicodedata import name
from django.shortcuts import render
from django.http import HttpResponse

from bb_public.models import EmailUpdateList, ContactUs

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
    new_email = EmailUpdateList(
        email=request.POST['email']
    )
    new_email.save()

    # return redirect('/')
    return HttpResponse('Email Submitted, Thank You', status=200)

def contact_us_form(request):
    '''
    URL: brickbox.io/forms/contact/
    Method: POST
    Args: name, email, message
    Recives and saves messages from the contact us form.
    '''
    new_message = ContactUs(
        name = request.POST.get('name'),
        email = request.POST.get('email'),
        message = request.POST.get('message')
    )
    new_message.save()

    return HttpResponse('Message Submitted, Thank You', status=200)

# ---------------------------------------------------------------------------- #
#                                      PWA                                     #
# ---------------------------------------------------------------------------- #

# ---------------------------------- Offline --------------------------------- #
def pwa_offline(request):
    '''
    URL: brickbox.io/offline/
    '''
    return render(request, 'pwa_offline.html')
