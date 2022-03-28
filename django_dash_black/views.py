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
                            ColocationClient, ResourceTimeTracking, BillingHistory,
                            CustomScript
)
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
    context['debug'] = settings.DEBUG

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))
