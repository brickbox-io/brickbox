''' Django Black Dashboard views_colo.py '''

import sys
import stripe

from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.template import loader
from django.http import HttpResponse
from django import template

from bb_data.models import UserProfile

if settings.DEBUG is False:
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripePubKey = settings.STRIPE_PUBLISHABLE_KEY
    stripe_clident_id = settings.CLIENT_ID
else:
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    stripePubKey = settings.STRIPE_PUBLISHABLE_KEY_TEST
    stripe_clident_id = settings.CLIENT_ID_TEST

if 'test' in sys.argv:
    current_domain = "examle.com"
else:
    current_domain = Site.objects.get_current().domain

@login_required(login_url="/login/")
def onboarding(request):
    '''
    URL: /dash/colo/
    Method: GET
    Returns the onboarding page for the Colo dashboard.
    '''
    context = {}
    try:
        profile = UserProfile.objects.get(user = request.user)

        first_colo = profile.clients.all()[0]
        print(first_colo)
        print(first_colo.stripe_account_id)

        if first_colo.stripe_account_id is None:
            new_account = stripe.Account.create(
                country = "US",
                type = "express",
                capabilities = {
                    "card_payments": {"requested": False},
                    "transfers": {"requested": True},
                },
                business_type = "individual",
                business_profile = {
                    "product_description": "Colocation at brickbox.io"
                },
                email = f"{request.user.email}",
                individual = {
                    "first_name": f"{request.user.first_name}",
                    "last_name": f"{request.user.last_name}",
                }
                # tos_acceptance = {"service_agreement": "recipient"},
            )

            first_colo.stripe_account_id = new_account.id
            first_colo.save()

        account_details = stripe.Account.retrieve(first_colo.stripe_account_id)
        print(account_details.details_submitted)
        if account_details.details_submitted is False:
            stripe_link = stripe.AccountLink.create(
                account = first_colo.stripe_account_id,
                refresh_url = f"https://{current_domain}/dash/colo",
                return_url = f"https://{current_domain}/dash/colo",
                type = "account_onboarding",
            )
            context["stripe_link_url"] = stripe_link.url
        else:
            context["stripe_link_url"] = False

        context["profile"] = profile
        context["first_colo"] = first_colo

        return render(request, 'colo.html', context)

    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))
