''' bb_billing - views_invoice.py '''

import json
import stripe

from django.shortcuts import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from bb_data.models import (
    UserProfile, ResourceTimeTracking, BillingHistory
)

@csrf_exempt
def invoice_event(request):
    '''
    URL: /stripe/invoice
    Processes invoice events from stripe.
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
        customer = UserProfile.objects.get(cus_id=invoice.customer)

        bill, created = BillingHistory.objects.get_or_create(
                            user = customer.user, invoice_id=invoice.id
                        )
        bill.status = 'paid'
        bill.invoice_link = invoice.invoice_pdf

        if created:
            bill.amount_alt = invoice.amount_due / 100

        bill.save()

        if not created:
            tracking = ResourceTimeTracking.objects.get(id=bill.usage.id)
            user_profile = UserProfile.objects.get(user=tracking.user)

            tracking.balance_paid = True
            tracking.stripe_transaction = invoice.charge
            tracking.save()

            if user_profile.threshold == 1.00:
                user_profile.threshold = 10.00

            elif user_profile.threshold == 10.00:
                user_profile.threshold = 100.00

            elif user_profile.threshold == 100.00:
                user_profile.threshold = 1000.00

            elif user_profile.threshold == 1000.00:
                user_profile.threshold = 0.00

            user_profile.save()


    elif event.type == 'invoice.payment_failed':
        invoice = event.data.object
        customer = UserProfile.objects.get(cus_id=invoice.customer)

        if customer.threshold == 1.00:
            customer.strikes = customer.strikes + 3

        if customer.threshold == 10.00:
            customer.strikes = customer.strikes + 2

        customer.save()

    else:
        print(f'Unhandled event type {event.type}')

    return HttpResponse(status=200)
