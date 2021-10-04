''' Processes account registration views. '''

from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import login, authenticate

from django.contrib.auth.forms import UserCreationForm

from bb_accounts.forms import RegistrationForm

from bb_data.models import UserProfile

def account_registration(request):
    '''
    URL: /register/
    Method: GET, POST
    Handles the creation of a new account.

    POST Variables:
        email
        password

    Response: Form Errors or Redirect
    '''
    if request.method not in ('POST', 'GET'):
        return HttpResponse(status=405)

    if request.user.is_authenticated:
        return HttpResponseRedirect('/dash/')

    if request.method == 'POST':
        print(request.POST)

        custom_request = {}
        custom_request['email'] = request.POST.get('email')
        custom_request['username'] = custom_request['email']
        custom_request['password1'] = request.POST.get('password')
        custom_request['password2'] = custom_request['password1']

        print(custom_request)

        form = RegistrationForm(custom_request)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            user_profile = UserProfile(
                                user = request.user,
                            )
            user_profile.save()

            return redirect('/dash/')

        print(form.errors)

    return render(request, 'registration/register.html', {'form_class':UserCreationForm})
