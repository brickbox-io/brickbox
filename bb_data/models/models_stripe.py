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
