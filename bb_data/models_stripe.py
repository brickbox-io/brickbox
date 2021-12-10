''' Defines how Stripe data is stored and managed. '''

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SavedPaymentMethod(models.Model):
    '''
    Records all available payment methods available for a user.
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey('bb_data.Profile', on_delete=models.CASCADE)

    # Stripe
    pm_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'Users Payment Methods'
