''' bb_billing - views_bb_billing.py '''

import stripe

from django.conf import settings
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

from bb_data.models import UserProfile, ResourceTimeTracking, BillingHistory, ResourceRates

if settings.DEBUG is False:
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripePubKey = settings.STRIPE_PUBLISHABLE_KEY
    stripe_clident_id = settings.CLIENT_ID
else:
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    stripePubKey = settings.STRIPE_PUBLISHABLE_KEY_TEST
    stripe_clident_id = settings.CLIENT_ID_TEST

@login_required
def manual_payment(request):
    '''
    URL: /bb_billing/manual_payment/
    Method: POST
    '''
    user_profile = UserProfile.objects.get(user=request.user)
    open_balance = ResourceTimeTracking.objects.filter(
                        user = request.user,
                        balance_paid = False
                    ).order_by('-id')[0]

     # 3070 Line Item
    if open_balance.minutes_3070 > 0:
        stripe.InvoiceItem.create(
            customer=user_profile.cus_id,
            currency='usd',
            description='GPU | 3070',
            quantity=int(float(open_balance.minutes_3070)/60),
            price=ResourceRates.objects.get(resource='3070').stripe_price_id,
        )

    # 3090 Line Item
    if open_balance.minutes_3090 > 0:
        stripe.InvoiceItem.create(
            customer=user_profile.cus_id,
            currency='usd',
            description='GPU | 3090',
            quantity=int(float(open_balance.minutes_3090)/60),
            price=ResourceRates.objects.get(resource='3090').stripe_price_id,
        )

    invoice = stripe.Invoice.create(
        customer=user_profile.cus_id,
        description="Monthly Resource Usage Invoice",
    )

    try:
        stripe.Invoice.pay(invoice.id)
    except stripe.error.CardError as err:
        return JsonResponse(
                    {
                        'notice': err.message,
                        'balance': open_balance.cycle_total,

                    },
                    status=200, safe=False
                )

    billing_record = BillingHistory(
                        user = open_balance.user,
                        usage = open_balance,
                        invoice_id = invoice.id,
                    )

    billing_record.save()

    return JsonResponse(
                {
                    'notice': 'Balance Paid',
                    'balance': 0,

                },
                status=200,
                safe=False
            )
