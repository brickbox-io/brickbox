''' Defines how Stripe data is stored and managed. '''

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PaymentMethod(models.Model):
    '''
    All stored paymetment methods
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pm_id = models.CharField(max_length=100, blank=True, null=True)

    brand = models.CharField(max_length=32, blank=True, null=True)
    last4 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = 'Payment Methods'
        app_label='bb_data'

class PaymentMethodOwner(models.Model):
    '''
    Records all available payment methods available for a user.
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey('bb_data.UserProfile', on_delete=models.CASCADE)
    method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)

    #Flags
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = 'Users Payment Methods'
        app_label='bb_data'

# ---------------------------------------------------------------------------- #
#                                    Billing                                   #
# ---------------------------------------------------------------------------- #

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

    rate_3070 = models.DecimalField(max_digits=5, decimal_places=2, default=0.50) # 3070 Rate/H
    rate_3090 = models.DecimalField(max_digits=5, decimal_places=2, default=0.75) # 3090 Rate/H

    balance_paid = models.BooleanField(default=False)
    stripe_transaction = models.CharField(max_length=100, blank=True, null=True) # Transaction ID

    @property
    def cycle_total(self):
        '''
        Returns the calculated total charge for the period.
        '''
        total_3070 = float(self.minutes_3070/60) * float(self.rate_3070)
        total_3090 = float(self.minutes_3090/60) * float(self.rate_3090)

        return "%0.2f" % round((total_3070+total_3090), 2) #pylint: disable=consider-using-f-string

    class Meta:
        verbose_name_plural = "Resource Time Tracking"
