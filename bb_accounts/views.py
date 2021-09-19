''' Processes account registration views. '''

from django.shortcuts import render

from django.http import HttpResponseRedirect

from django.contrib.auth.forms import UserCreationForm



def account_registration(request):
    '''
    URL: /register/
    Handles the creation of a new account.
    '''
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dash/')
    else:
        return render(request, 'registration/register.html', {'form_class':UserCreationForm})
