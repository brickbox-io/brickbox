''' bb_billing - views_payment_method.py '''

import json
import stripe

from django.shortcuts import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from bb_data.models import (
    UserProfile, ColocationClient, PaymentMethod,
    PaymentMethodOwner, ResourceTimeTracking, BillingHistory
)

@csrf_exempt
def payment_method_event(request):
    '''
    URL: /stripe/payment_method
    '''
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_method.attached':
        payment_method = event.data.object
        print(payment_method)

        profile = UserProfile.objects.get(cus_id=payment_method.customer)

        payment_method = PaymentMethod(
            user = profile.user,
            pm_id = payment_method.id,
            brand = payment_method.card.brand,
            last4 = payment_method.card.last4,
        )
        payment_method.save()

        PaymentMethodOwner.objects.create(
            user = profile.user,
            profile = profile,
            method = payment_method,
        )

        stripe.Customer.modify(
            profile.cus_id,
            invoice_settings = {
                "default_payment_method": payment_method.pm_id,
            }
        )

    return HttpResponse(status=200)
