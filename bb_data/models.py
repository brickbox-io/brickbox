''' models.py for bb_data '''

import requests

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

User = get_user_model()

# ----------------------------- Selection Options ---------------------------- #
crypto_options = (
    ('eth', 'ethereum'),
)

fiat_options = (
    ('$', 'United States Dollar'),
)


class UserProfile(models.Model):
    '''
    Any user related settings, prefrences.
    '''
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    clients = models.ManyToManyField(
                                    'ColocationClient',
                                    through='ColocationClientOwner',
                                    related_name='clients_owned'
                                    )


class ColocationClient(models.Model):
    '''
    The business or individual that owns the equipment under management.
    '''
    account_name = models.CharField(max_length = 124)
    owners = models.ManyToManyField(
                                    'UserProfile',
                                    through='ColocationClientOwner',
                                    related_name='client_owners'
                                    )

    vast_api_key = models.CharField(max_length = 64, blank=True, null=True)
    eth_deposit_address = models.CharField(max_length = 64, blank=True, null=True)

    def __str__(self):
        return f"{self.account_name } ({self.id})"


class ColocationClientOwner(models.Model):
    '''
    Pairs client accounts with a user.
    '''
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    owner_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    client_account = models.ForeignKey(ColocationClient, on_delete=models.DO_NOTHING)

class CryptoSnapshot(models.Model):
    '''
    Used to store an ammount of crypto held at a specific time.
    '''
    recorded = models.DateTimeField(auto_now_add=True)
    account_holder = models.ForeignKey(ColocationClient, on_delete=models.DO_NOTHING)
    balance = models.DecimalField(max_digits=64, decimal_places=32)
    currency = models.CharField(max_length=3, choices=crypto_options)

    dollar_price = models.DecimalField(max_digits=32, decimal_places=2, blank=True, null=True)

    start_period = models.BooleanField(default=False)

@receiver(post_save, sender=CryptoSnapshot)
def grab_crypto_price(sender, instance, created, **kwargs):
    '''
    On new snapshot, auto adds the value of the crypto.
    '''
    print(f"Send by {sender}")
    if created:
        eth = requests.get('https://api.etherscan.io/api?module=stats&action=ethprice').json()
        eth_price = eth['result']['ethusd']
        instance.dollar_price = eth_price
        instance.save()

@receiver(post_save, sender=CryptoSnapshot)
def check_new_period_crypto(sender, instance, created, **kwargs):
    '''
    Marks snapshot as starting period if balance is lower than previous entry.
    '''
    print(f"Send by {sender}")
    if created:
        previous_records = CryptoSnapshot.objects.filter(
            account_holder = instance.account_holder).order_by('-id')[:2]

        if previous_records[0].balance < previous_records[1].balance:
            instance.start_period = True
            instance.save()


class FiatSnapshot(models.Model):
    '''
    Used to store an ammount of fiat currency held at a specific time.
    '''
    recorded = models.DateTimeField(auto_now_add=True)
    account_holder = models.ForeignKey(ColocationClient, on_delete=models.DO_NOTHING)
    balance = models.DecimalField(max_digits=32, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=1, choices=fiat_options)

    start_period = models.BooleanField(default=False)

@receiver(post_save, sender=FiatSnapshot)
def check_new_period_fiat(sender, instance, created, **kwargs):
    '''
    Marks snapshot as starting period if balance is lower than previous entry.
    '''
    print(f"Send by {sender}")
    if created:
        previous_records = FiatSnapshot.objects.filter(
            account_holder = instance.account_holder).order_by('-id')[:2]

        if previous_records[0].balance < previous_records[1].balance:
            instance.start_period = True
            instance.save()
