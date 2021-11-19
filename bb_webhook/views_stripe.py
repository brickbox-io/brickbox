''' Processes webhooks from Stripe '''

import stripe
import json

from django.shortcuts import render, HttpResponse

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



    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object # contains a stripe.PaymentIntent
        # Then define and call a method to handle the successful payment intent.
        # handle_payment_intent_succeeded(payment_intent)
    elif event.type == 'payment_method.attached':
        payment_method = event.data.object # contains a stripe.PaymentMethod
        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)
        # ... handle other event types
    else:
        print(f'Unhandled event type {event.type}')

    return HttpResponse(status=200)
