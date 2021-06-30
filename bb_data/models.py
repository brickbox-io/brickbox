''' models.py for bb_data '''

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save

crypto_options = (
    ('eth', 'ethereum'),
)

fiat_options = (
    ('$', 'United States Dollar'),
)

class ColocationClient(models.Model):
    '''
    The business or individual that owns the equipment under management.
    '''
    account_name = models.CharField(max_length = 124)


class CryptoSnapshot(models.Model):
    '''
    Used to store an ammount of crypto held at a specific time.
    '''
    recorded = models.DateTimeField(auto_now_add=True)
    account_holder = models.ForeignKey(ColocationClient, on_delete=models.DO_NOTHING)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=crypto_options)

    dollar_price = models.DecimalField(max_digits=10, decimal_places=2)

@reciver(pre_save, sender=CryptoSnapshot)
def grab_crypto_price(sender, instance, created, **kwargs):
    '''
    On new snapshot, auto adds the value of the crypto.
    '''
    if created:

        instance.dollar_price =
        instance.save()

class FiatSnapshot(models.Model):
    '''
    Used to store an ammount of fiat currency held at a specific time.
    '''
    recorded = models.DateTimeField(auto_now_add=True)
    account_holder = models.ForeignKey(ColocationClient, on_delete=models.DO_NOTHING)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=1, choices=fiat_options)
