''' bb_billing - views_payment_method.py '''

import json
import stripe

from django.shortcuts import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from django.core.exceptions import ValidationError

from bb_data.models import (
    UserProfile, PaymentMethod,
    PaymentMethodOwner)

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
        stripe_payment_method = event.data.object
        profile = UserProfile.objects.get(cus_id=stripe_payment_method.customer)

        try:
            # New card will be validated, then set as default
            payment_method = PaymentMethod(
                user = profile.user,
                pm_id = stripe_payment_method.id,
                brand = stripe_payment_method.card.brand,
                last4 = stripe_payment_method.card.last4,
                fingerprint = stripe_payment_method.card.fingerprint,
                is_default = True
            )

            payment_method.full_clean()

        except ValidationError:
            stripe.PaymentMethod.detach(
                stripe_payment_method.id
            )
            return HttpResponse(status=200)

        # Remove previous default payment method
        PaymentMethod.objects.filter(
            user = profile.user,
            is_default = True
        ).update(is_default = False)

        payment_method.save()

        # Assign payment method to user
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
