'''
Handles Stripe related functions.
'''

import stripe

from django.conf import settings
from django.http import HttpResponse

from bb_data.models import UserProfile


if settings.DEBUG is False:
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripePubKey = settings.STRIPE_PUBLISHABLE_KEY
    stripe_clident_id = settings.CLIENT_ID
else:
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    stripePubKey = settings.STRIPE_PUBLISHABLE_KEY_TEST
    stripe_clident_id = settings.CLIENT_ID_TEST


def method(request):
    '''
    URL: /data/stripe/pay/method
    '''
    print(request)

    profile = UserProfile.objects.get(user=request.user)

    if not profile.cus_id:
        new_customer = stripe.Customer.create()

        profile.cus_id = new_customer.id
        profile.save()

    intent = stripe.SetupIntent.create(
        customer = profile.cus_id,
        payment_method_types = ["bancontact", "card", "ideal"],
    )

    return HttpResponse(intent.client_secret, status=200)


# def method_sucess(request):
#     '''
#     URL: /data/stripe/pay/method/success
#     '''
#     print(request)

#     return HttpResponse(intent.client_secret, status=200)
