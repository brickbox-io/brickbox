''' Defines how Stripe data is stored and managed. '''

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# ----------------------------- Selection Options ---------------------------- #
invoice_status_choices = (
    ('unpaid', 'Unpaid'),
    ('paid', 'Paid'),
)

# ------------------------------ Payment Method ------------------------------ #
class PaymentMethod(models.Model):
    '''
    All stored paymetment methods
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pm_id = models.CharField(max_length=100, blank=True, null=True)

    brand = models.CharField(max_length=32, blank=True, null=True)
    last4 = models.IntegerField(blank=True, null=True)

    #Flags
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = 'Payment Methods'
        app_label='bb_data'

# --------------------------- Payment Method Owner --------------------------- #
class PaymentMethodOwner(models.Model):
    '''
    Records all available payment methods available for a user.
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey('bb_data.UserProfile', on_delete=models.CASCADE)
    method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = 'Users Payment Methods'
        app_label='bb_data'

# ---------------------------------------------------------------------------- #
#                                    Billing                                   #
# ---------------------------------------------------------------------------- #

class ResourceRates(models.Model):
    '''
    Contains the rate options for resources.
    '''
    resource = models.CharField(max_length=32, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=100, blank=True, null=True)

class ResourceTimeTracking(models.Model):
    '''
    Record of resource time used within a billing period.
    *Might want to tie this to the VM later*
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    billing_cycle_start = models.DateField(auto_now_add=True)
    billing_cycle_end = models.DateField(null=True)

    minutes_3070 = models.IntegerField(default=0)   # Running total of active 3070 usage
    minutes_3090 = models.IntegerField(default=0)   # Running total of active 3090 usage

    rate_3070 = models.DecimalField(max_digits=8, decimal_places=2, default=0.50) # 3070 Rate/H
    rate_3090 = models.DecimalField(max_digits=8, decimal_places=2, default=0.75) # 3090 Rate/H

    balance_paid = models.BooleanField(default=False)
    stripe_transaction = models.CharField(max_length=100, blank=True, null=True) # Transaction ID

    destroy_vms_countdown_started = models.BooleanField(default=False)

    @property
    def cycle_total(self):
        '''
        Returns the calculated total charge for the period.
        '''
        total_3070 = int(self.minutes_3070/60) * float(self.rate_3070)
        total_3090 = int(self.minutes_3090/60) * float(self.rate_3090)

        return float("%0.2f" % round((total_3070+total_3090), 2)) #pylint: disable=consider-using-f-string

    class Meta:
        verbose_name_plural = "Resource Time Tracking"

class BillingHistory(models.Model):
    '''
    Maintains a record of billing invoices.
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    usage = models.ForeignKey(ResourceTimeTracking, on_delete=models.CASCADE, blank=True,null=True)
    amount_alt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    invoice_number = models.CharField(max_length=100, blank=True, null=True) # Stripe Invoice No.
    invoice_link = models.TextField(blank=True, null=True)
    invoice_id = models.CharField(max_length=100, blank=True, null=True)     # Stripe Invoice ID

    status = models.CharField(max_length=32, choices=invoice_status_choices, default='unpaid')

    class Meta:
        verbose_name_plural = 'Billing History'

# @reciver(post_save, sender=BillingHistory)
# def update_tracking_paid_status(sender, instance, created,**kwargs):
#     '''
#     Updates the ResourceTimeTracking record to reflect the status of the invoice.
#     '''
#     if instance.status == 'paid':
#         instance.usage.balance_paid = True
#         instance.usage.save()
