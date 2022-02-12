''' Processes webhooks from Stripe '''

import json
import stripe

from django.shortcuts import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from bb_data.models import (
    UserProfile, ColocationClient, PaymentMethod,
    PaymentMethodOwner, ResourceTimeTracking, BillingHistory
)


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

@csrf_exempt
def payment_method_event(request):
    '''
    URL: webhook/stripe/payment_method
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

@csrf_exempt
def invoice_event(request):
    '''
    URL: webhook/stripe/invoice_event
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
    if event.type == 'invoice.payment_succeeded':
        invoice = event.data.object
        #print(invoice)
        bill = BillingHistory.objects.get(invoice_id=invoice.id)
        bill.status = 'paid'
        bill.invoice_link = invoice.invoice_pdf
        bill.save()

        tracking = ResourceTimeTracking.objects.get(id=bill.usage.id)
        tracking.balance_paid = True
        tracking.stripe_transaction = invoice.charge

        if tracking.threshold == 1.00:
            tracking.threshold = 10.00

        elif tracking.threshold == 10.00:
            tracking.threshold = 100.00

        elif tracking.threshold == 100.00:
            tracking.threshold = 1000.00

        elif tracking.threshold == 1000.00:
            tracking.threshold = 0.00

        tracking.save()


    elif event.type == 'invoice.payment_failed':
        invoice = event.data.object
        print(invoice)
    else:
        print(f'Unhandled event type {event.type}')

    return HttpResponse(status=200)
