''' Tasks relating to the billing process. '''
from __future__ import absolute_import, unicode_literals

import datetime

import stripe

from django.conf import settings

from celery import shared_task

from bb_data.models import UserProfile, ResourceRates, ResourceTimeTracking, BillingHistory

if settings.DEBUG is False:
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripePubKey = settings.STRIPE_PUBLISHABLE_KEY
    stripe_clident_id = settings.CLIENT_ID
else:
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    stripePubKey = settings.STRIPE_PUBLISHABLE_KEY_TEST
    stripe_clident_id = settings.CLIENT_ID_TEST

@shared_task
def threshold_resource_invoicing():
    '''
    Ran against the time tracking model to determine if a resource has exceeded their threshold.
    '''
    invoices_due = ResourceTimeTracking.objects.filter(
                                    balance_paid = False,
                                )

    for invoice_due in invoices_due:
        user_profile = UserProfile.objects.get(user=invoice_due.user)

        # Indicates the user is month to month or on the credit system.
        if user_profile.threshold == 0 or user_profile.strikes >= 3:
            continue

        if user_profile.user.is_superuser or not user_profile.pay_methods.exists():
            continue

        if user_profile.cus_id and user_profile.threshold <= float(invoice_due.cycle_total) > 0:

            # 3070 Line Item
            if invoice_due.minutes_3070 > 0:
                stripe.InvoiceItem.create(
                    customer=user_profile.cus_id,
                    currency='usd',
                    description='GPU | 3070',
                    quantity=int(float(invoice_due.minutes_3070)/60),
                    price=ResourceRates.objects.get(resource='3070').stripe_price_id,
                    # amount=int(float(invoice_due.minutes_3070/60) * float(invoice_due.rate_3070)),
                )

            # 3090 Line Item
            if invoice_due.minutes_3090 > 0:
                stripe.InvoiceItem.create(
                    customer=user_profile.cus_id,
                    currency='usd',
                    description='GPU | 3090',
                    quantity=int(float(invoice_due.minutes_3090)/60),
                    price=ResourceRates.objects.get(resource='3090').stripe_price_id,
                    # amount=int(float(invoice_due.minutes_3090/60) * float(invoice_due.rate_3090)),
                )

            invoice = stripe.Invoice.create(
                customer=user_profile.cus_id,
                description="Monthly Resource Usage Invoice",
            )

            try:
                stripe.Invoice.pay(invoice.id)
            except stripe.error.CardError as err:
                print(err)

            billing_record = BillingHistory(
                                user = invoice_due.user,
                                usage = invoice_due,
                                invoice_id = invoice.id,
                            )

            billing_record.save()

@shared_task
def monthly_resource_invoicing():
    '''
    Ran against the time tracking model to collect payment on resources consumed over a month.
    '''
    invoices_due = ResourceTimeTracking.objects.filter(
                                    balance_paid = False,
                                    billing_cycle_end__lte=datetime.datetime.today(),
                                )
    for invoice_due in invoices_due:
        user_profile = UserProfile.objects.get(user=invoice_due.user)

        if user_profile.user.is_superuser or not user_profile.pay_methods.exists():
            continue

        if user_profile.cus_id and float(invoice_due.cycle_total) > 0:

            # 3070 Line Item
            if invoice_due.minutes_3070 > 0:
                stripe.InvoiceItem.create(
                    customer=user_profile.cus_id,
                    currency='usd',
                    description='GPU | 3070',
                    quantity=int(float(invoice_due.minutes_3070)/60),
                    price=ResourceRates.objects.get(resource='3070').stripe_price_id,
                    # amount=int(float(invoice_due.minutes_3070/60) * float(invoice_due.rate_3070)),
                )

            # 3090 Line Item
            if invoice_due.minutes_3090 > 0:
                stripe.InvoiceItem.create(
                    customer=user_profile.cus_id,
                    currency='usd',
                    description='GPU | 3090',
                    quantity=int(float(invoice_due.minutes_3090)/60),
                    price=ResourceRates.objects.get(resource='3090').stripe_price_id,
                    # amount=int(float(invoice_due.minutes_3090/60) * float(invoice_due.rate_3090)),
                )

            invoice = stripe.Invoice.create(
                customer=user_profile.cus_id,
                description="Monthly Resource Usage Invoice",
            )

            try:
                stripe.Invoice.pay(invoice.id)
            except stripe.error.CardError as err:
                if err.code == 'card_declined':
                    user_profile.strikes += 1
                    user_profile.save()


            billing_record = BillingHistory(
                                user = invoice_due.user,
                                usage = invoice_due,
                                invoice_id = invoice.id,
                            )

            billing_record.save()
