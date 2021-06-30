''' models.py for bb_data '''

import requests

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# ----------------------------- Selection Options ---------------------------- #
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
    vast_api_key = models.CharField(max_length = 64, blank=True, null=True)
    eth_deposit_address = models.CharField(max_length = 64, blank=True, null=True)

    def __str__(self):
        return f"{self.account_name } ({self.id})"


class CryptoSnapshot(models.Model):
    '''
    Used to store an ammount of crypto held at a specific time.
    '''
    recorded = models.DateTimeField(auto_now_add=True)
    account_holder = models.ForeignKey(ColocationClient, on_delete=models.DO_NOTHING)
    balance = models.DecimalField(max_digits=64, decimal_places=32)
    currency = models.CharField(max_length=3, choices=crypto_options)

    dollar_price = models.DecimalField(max_digits=32, decimal_places=2, blank=True, null=True)

@receiver(post_save, sender=CryptoSnapshot)
def grab_crypto_price(sender, instance, created, **kwargs):
    '''
    On new snapshot, auto adds the value of the crypto.
    '''
    if created:
        eth = requests.get('https://api.etherscan.io/api?module=stats&action=ethprice').json()
        eth_price = eth['result']['ethusd']
        instance.dollar_price = eth_price
        instance.save()


class FiatSnapshot(models.Model):
    '''
    Used to store an ammount of fiat currency held at a specific time.
    '''
    recorded = models.DateTimeField(auto_now_add=True)
    account_holder = models.ForeignKey(ColocationClient, on_delete=models.DO_NOTHING)
    balance = models.DecimalField(max_digits=32, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=1, choices=fiat_options)
