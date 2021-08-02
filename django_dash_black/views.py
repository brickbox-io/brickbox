# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from itertools import chain
from operator import attrgetter

from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
from django import template

from bb_data.models import UserProfile, CryptoPayout, FiatPayout

@login_required(login_url="/login/")
def index(request):
    '''
    Dashboard index
    '''
    context = {}
    context['profile'] = UserProfile.objects.get(user = request.user)

    # Only grabs the first client for now until there is a proper way to dysplay multiple.
    try:
        context['client'] = UserProfile.objects.get(user = request.user).clients.all()[0]
    except IndexError:
        context['client'] = None

    # ------------------------------ Payout History ------------------------------ #
    crypto_payout = CryptoPayout.objects.filter(account_holder=context['client'])
    fiat_payout = FiatPayout.objects.filter(account_holder=context['client'])

    context['history'] = sorted(chain(crypto_payout, fiat_payout), key=attrgetter('dated'))

    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    '''
    Serves the diffrent pages.
    '''
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    # except:

    #     html_template = loader.get_template( 'page-500.html' )
    #     return HttpResponse(html_template.render(context, request))
