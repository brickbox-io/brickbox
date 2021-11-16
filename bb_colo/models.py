''' bb_colo models.py '''

from django.db import models
from django.contrib.auth import get_user_model

from bb_data.models import UserProfile, ColocationClient

User = get_user_model()

# --------------------------- colo Onboarding Stage -------------------------- #
class colocationOnboarding(models.Model):
    '''
    Used to track the stage of a client coming on as a CoLo.
    '''
    client = models.ForeignKey(ColocationClient, on_delete=models.CASCADE)

    lease_signature = models.BooleanField(default=False)
    nda_signature = models.BooleanField(default=False)
    usd_payout_info = models.BooleanField(default=False)
    crypto_payout_info = models.BooleanField(default=False)
    first_unit_ordered = models.BooleanField(default=False)
    insurance_info_received = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.client.owner_profile.user}'

    class Meta:
        verbose_name = 'Colocation Onboarding'
