''' models.py for bb_data '''

import json
import time
import requests

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

User = get_user_model()

# ----------------------------- Selection Options ---------------------------- #
crypto_options = (
    ('eth', 'Ethereum'),
)

fiat_options = (
    ('$', 'United States Dollar'),
)


# ------------------------------- User Profile ------------------------------- #
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

    brick_access = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user})"

    class Meta:
        verbose_name_plural = "User Profiles"

# ---------------------------------- Client ---------------------------------- #
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
        return f"{self.account_name } (ID: {self.id})"

    class Meta:
        verbose_name_plural = "Colocation Clients"


# ------------------------------- Client Owner ------------------------------- #
class ColocationClientOwner(models.Model):
    '''
    Pairs client accounts with a user.
    '''
    # owner = models.ForeignKey(User, on_delete=models.CASCADE)
    owner_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    client_account = models.ForeignKey(ColocationClient, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "Colocation Client Owners"
        unique_together = ('owner_profile', 'client_account')


# ---------------------------------------------------------------------------- #
#                                Blance Records                                #
# ---------------------------------------------------------------------------- #

# ---------------------------------- Crypto ---------------------------------- #
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

    class Meta:
        verbose_name_plural = "Crypto Snapshot"

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


# ----------------------------------- Fiat ----------------------------------- #
class FiatSnapshot(models.Model):
    '''
    Used to store an ammount of fiat currency held at a specific time.
    '''
    recorded = models.DateTimeField(auto_now_add=True)
    account_holder = models.ForeignKey(ColocationClient, on_delete=models.DO_NOTHING)
    balance = models.DecimalField(max_digits=32, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=1, choices=fiat_options)

    start_period = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Fiat Snapshot"

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


# ---------------------------------------------------------------------------- #
#                             Track Payout History                             #
# ---------------------------------------------------------------------------- #

# ---------------------------------- Crypto ---------------------------------- #
class CryptoPayout(models.Model):
    '''
    Records a timestamp and ammount when a client recives a distribution of crypto.
    '''
    recorded = models.DateTimeField(auto_now_add=True)
    dated = models.DateTimeField(null=True)
    account_holder = models.ForeignKey(ColocationClient, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=64, decimal_places=32)
    currency = models.CharField(max_length=3, choices=crypto_options)

    tx_hash = models.CharField(max_length = 66, unique=True)

    dollar_price = models.DecimalField(max_digits=32, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Crypto Payouts"

# ----------------------------------- Fiat ----------------------------------- #
class FiatPayout(models.Model):
    '''
    Records a timestamp and ammount when a client recives a distribution of fiat.
    '''
    recorded = models.DateTimeField(auto_now_add=True)
    dated = models.DateTimeField(null=True)
    account_holder = models.ForeignKey(ColocationClient, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=32, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=1, choices=fiat_options)

    tx_vast_id = models.CharField(max_length = 66, unique=True, null=True)

    class Meta:
        verbose_name_plural = "Fiat Payouts"


@receiver(post_save, sender=CryptoPayout)
@receiver(post_save, sender=CryptoSnapshot)
def grab_crypto_price(sender, instance, created, **kwargs):
    '''
    On new snapshot, auto adds the value of the crypto.
    '''
    print(f"Send by {sender}")
    if created:

        eth_price = 0

        try:
            eth_result = requests.get('https://api.etherscan.io/api?module=stats&action=ethprice')

            eth = json.loads(eth_result.text)
            eth_price = eth['result']['ethusd']

        except TypeError:
            time.sleep(60)
            eth_result = requests.get('https://api.etherscan.io/api?module=stats&action=ethprice')

            eth = json.loads(eth_result.text)
            eth_price = eth['result']['ethusd']



        if sender == CryptoSnapshot:
            instance.dollar_price = float(instance.balance)*float(eth_price)

        if sender == CryptoPayout:
            instance.dollar_price = float(instance.amount)*float(eth_price)

        instance.save()
