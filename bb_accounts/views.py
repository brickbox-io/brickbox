''' Processes account registration views. '''

from google.oauth2 import id_token
from google.auth.transport import requests

from allauth.socialaccount.models import SocialAccount

from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError

from django.conf import settings

from django.contrib.auth import login, authenticate, get_user_model

from django.contrib.auth.forms import UserCreationForm

from bb_accounts.forms import RegistrationForm

from bb_data.models import UserProfile

User = get_user_model()


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
                                brick_access = True,
                                is_beta = True,
                            )
            user_profile.save()

            return redirect('/dash/')

        print(form.errors)
        return render(request, 'registration/register.html',
                    {'form_class':UserCreationForm, 'form_errors':form.errors}
                )

    return render(request, 'registration/register.html', {'form_class':UserCreationForm})


@csrf_exempt
def token_signin(request):
    '''
    URL: /tokensignin/
    Method: AJAX
    Processes Google authentication token when registering.
    '''
    if request.method == "GET":
        return HttpResponse(status=405)

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(
                    request.POST.get('credential'), requests.Request(),
                    settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id'])

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']

        if SocialAccount.objects.filter(uid = userid).exists():
            print('Account already connected.')
            social_user = SocialAccount.objects.get(uid=userid)
            login(
                request,
                social_user.user,
                backend = 'allauth.account.auth_backends.AuthenticationBackend',
            )
            return redirect('/dash/')

        if not idinfo['email']:
            return HttpResponseServerError('No email returned.')

        try:
            new_user = User.objects.create_user(
                username = idinfo['email'],
                first_name = idinfo['given_name'],
                last_name = idinfo['family_name'],
                email = idinfo['email'],
            )
        except KeyError:
            new_user = User.objects.create_user(
                username = idinfo['email'],
                email = idinfo['email'],
            )

        new_socialaccount = SocialAccount(
            user = new_user,
            provider = 'google',
            uid = userid,
            extra_data = idinfo
        )

        new_socialaccount.save()

        login(
            request,
            new_socialaccount,
            backend = 'allauth.account.auth_backends.AuthenticationBackend'
        )

        user_profile = UserProfile(
                            user = new_user,
                            brick_access = True,
                            is_beta = True,
                        )
        user_profile.save()

        return redirect('/dash/')

    except ValueError as err:
        print(err)

        return HttpResponseServerError()
