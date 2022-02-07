''' Django Black Dashboard views.py '''

import datetime

from itertools import chain
from operator import attrgetter

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
from django import template

from bb_data.models import ( UserProfile, CryptoPayout, FiatPayout,
                            ColocationClient, ResourceTimeTracking, BillingHistory)
from bb_vm.models import VirtualBrickOwner, GPU, RentedGPU

if settings.DEBUG:
    stripe_pk = settings.STRIPE_PUBLISHABLE_KEY_TEST
else:
    stripe_pk = settings.STRIPE_PUBLISHABLE_KEY

@login_required()
def index(request, colo=0):
    '''
    Dashboard index
    '''
    context = {}

    try:
        context['profile'] = UserProfile.objects.get(user = request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(
                            user = request.user,
                        )
        user_profile.save()

        context['profile'] = user_profile

    # ------------------------------ Cycyle Balance ------------------------------ #
    tracker, created = ResourceTimeTracking.objects.get_or_create(
                                    user = context['profile'].user,
                                    balance_paid = False,
                                    billing_cycle_end__gte=datetime.datetime.today()
                                )
    if created:
        tracker.billing_cycle_end = tracker.billing_cycle_start + datetime.timedelta(days=30)
        tracker.save()

    context['tracker'] = tracker


    # Only grabs the first client for now until there is a proper way to dysplay multiple.
    try:
        context['client'] = context['profile'].clients.all()[colo]
    except IndexError:
        context['client'] = None

    # ------------------------------ Payout History ------------------------------ #
    crypto_payout = CryptoPayout.objects.filter(account_holder=context['client'])
    fiat_payout = FiatPayout.objects.filter(account_holder=context['client'])

    context['history'] = sorted(chain(
                                        crypto_payout, fiat_payout),
                                        key=attrgetter('dated'),
                                        reverse=True
                                    )
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required()
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

        context['profile'] = UserProfile.objects.get(user = request.user)
        context['bricks'] = VirtualBrickOwner.objects.filter(owner=context['profile'])
        context['ssh_url'] = settings.SSH_URL

        context['colo_clients'] = ColocationClient.objects.all()

        context['stripe_pk'] = stripe_pk

        context['3090_gpu_available'] = False
        for gpu in GPU.objects.filter(model="3090", host__is_enabled=True, host__is_ready=True):
            if RentedGPU.objects.filter(gpu=gpu).count() < 1:
                context['3090_gpu_available'] = True

        context['3070_gpu_available'] = False
        for gpu in GPU.objects.filter(model="3070", host__is_enabled=True, host__is_ready=True):
            if RentedGPU.objects.filter(gpu=gpu).count() < 1:
                context['3070_gpu_available'] = True

        # ------------------------------ Cycyle Balance ------------------------------ #
        tracker, created = ResourceTimeTracking.objects.get_or_create(
                                        user = context['profile'].user,
                                        balance_paid = False,
                                        billing_cycle_end__gte=datetime.datetime.today()
                                    )
        context['billing_history'] = BillingHistory.objects.filter(user=context['profile'].user)

        if created:
            tracker.billing_cycle_end = tracker.billing_cycle_start + datetime.timedelta(days=30)
            tracker.save()

        context['tracker'] = tracker

        html_template = loader.get_template( f'{load_template}.html' )
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    # except:

    #     html_template = loader.get_template( 'page-500.html' )
    #     return HttpResponse(html_template.render(context, request))
