''' bb_billing - views_invoice.py '''

# pylint: disable=R0912,R0915

import json
import stripe

from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from bb_tasks.tasks import(pause_vm_subprocess, destroy_vm_with_open_tabs)

from bb_data.models import (
    UserProfile, ResourceTimeTracking, BillingHistory
)
from bb_vm.models import (
    VirtualBrickOwner,
)

@csrf_exempt
def invoice_event(request):
    '''
    URL: /stripe/invoice
    Processes invoice events from stripe webhooks.
    '''
    try:
        payload = request.body
        event = None
        event = stripe.Event.construct_from(
                    json.loads(payload), stripe.api_key
                )
    except ValueError:
        return HttpResponse(status=400) # Invalid payload

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
        else:
            tracking = ResourceTimeTracking.objects.get(id=bill.usage.id)
            user_profile = UserProfile.objects.get(user=tracking.user)

            tracking.balance_paid = True
            tracking.stripe_transaction = invoice.charge
            tracking.save()

            # Update threshold limit
            if 0.00 < user_profile.threshold < 1000.00:
                user_profile.threshold = user_profile.threshold*10
            else:
                user_profile.threshold = 0.00

            user_profile.save()

        bill.save()

    elif event.type == 'invoice.payment_failed':
        invoice = event.data.object
        customer = UserProfile.objects.get(cus_id=invoice.customer)

        # ------------------------------- $1 Threshold ------------------------------- #
        if customer.threshold == 1.00:
            customer.strikes = customer.strikes + 3
            countdown_time=86400 # VMs destroyed if balance is not paid within 24 hours

        # ------------------------------- $10 Threshold ------------------------------- #
        if customer.threshold == 10.00:
            customer.strikes = customer.strikes + 2
            countdown_time=172800 # VMs destroyed if balance is not paid within 48 hours

        # ------------------------------ $100 Threshold ------------------------------ #
        if customer.threshold == 100.00:
            customer.strikes = customer.strikes + 1
            countdown_time=432000 # VMs destroyed if balance is not paid within 5 days

        # ----------------------------- $1,000 Threshold ----------------------------- #
        if customer.threshold == 1000.00:
            countdown_time=259200 # VMs destroyed if balance is not paid within 3 days


        # -------------------------------- Suspend VMs ------------------------------- #
        if customer.threshold < 1000.00:
            owned_bricks = VirtualBrickOwner.objects.filter(owner=customer)
            for brick in owned_bricks:
                pause_vm_subprocess.apply_async(
                    (brick.virt_brick.id,),
                    queue='ssh_queue'
                )
                brick.virt_brick.is_on=False
                brick.virt_brick.save()

        # -------------------------------- Destroy VMs ------------------------------- #
        bill = BillingHistory.objects.get(invoice_id=invoice.id)
        tacker = ResourceTimeTracking.objects.get(id=bill.usage.id)
        if not tacker.destroy_vms_countdown_started:
            destroy_vm_with_open_tabs.apply_async(
                (tacker.id,),
                countdown=countdown_time,
                queue='ssh_queue'
            )
            tacker.destroy_vms_countdown_started = True
            tacker.save()

        customer.save()

    else:
        print(f'Unhandled event type {event.type}')

    return HttpResponse(status=200)
