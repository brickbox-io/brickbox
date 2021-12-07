''' Processes webhooks from Stripe '''

import json
import stripe

from django.shortcuts import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from bb_data.models import ColocationClient


@csrf_exempt
def account_event(request):
    '''
    URL: webhook/stripe/account
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

    # Account Updated
    if event.type == 'account.updated':
        account = event.data.object.id
        account_details = stripe.Account.retrieve(account)

        if account_details.details_submitted:
            ColocationClient.objects.filter(stripe_account_id=account).update(
                stripe_connected=True
            )

        return HttpResponse(status=200)


    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object # contains a stripe.PaymentIntent
        print(payment_intent)
        # Then define and call a method to handle the successful payment intent.
        # handle_payment_intent_succeeded(payment_intent)
    elif event.type == 'payment_method.attached':
        payment_method = event.data.object # contains a stripe.PaymentMethod
        print(payment_method)
        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)
        # ... handle other event types
    else:
        print(f'Unhandled event type {event.type}')

    return HttpResponse(status=200)
