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

    # SSH
    keys = models.ManyToManyField('SSHKey', through='SSHKeyOwner', related_name='keys_owned')

    # Flags
    brick_access = models.BooleanField(default=False)   # Brcik VM Access
    is_colo = models.BooleanField(default=False)        # "Investor"
    is_manager = models.BooleanField(default=False)     # Can manage colocation clients
    is_beta = models.BooleanField(default=False)        # Beta Access User

    # Stripe
    cus_id = models.CharField(max_length=100, blank=True, null=True)

    pay_methods = models.ManyToManyField(
                                                'bb_data.PaymentMethod',
                                                through='bb_data.PaymentMethodOwner',
                                                related_name='payment_methods_saved'
                                            )

    # Billing Threshold - $0.00 indicates no threshold (month to month)
    threshold = models.DecimalField(max_digits=8, decimal_places=2, default=1.00)

    # Used to mark problematic users, including failed payments.
    # 3+ strikes indicates the account is on the pre-credit system.
    strikes = models.IntegerField(default=0)
    credit_balance = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user})"

    class Meta:
        verbose_name_plural = "User Profiles"
        app_label='bb_data'

# --------------------------------- SSH Keys --------------------------------- #
class SSHKey(models.Model):
    '''
    SSH Keys for users.
    '''
    name = models.CharField(max_length=100, blank=True,)
    pub_key = models.TextField(max_length=5000, unique=True)

class SSHKeyOwner(models.Model):
    '''
    The owner of a SSH Key.
    '''
    profile = models.ForeignKey(UserProfile, related_name='profile', on_delete=models.CASCADE)
    key = models.ForeignKey(SSHKey, related_name='key', on_delete=models.CASCADE)

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

    term_agreement = models.BooleanField(default=False)

    stripe_account_id = models.CharField(max_length=128, blank=True, null=True)
    stripe_connected = models.BooleanField(default=False) # Verify user connected Stripe

    vast_api_key = models.CharField(max_length = 64, blank=True, null=True)
    eth_deposit_address = models.CharField(max_length = 64, blank=True, null=True)

    equipment = models.ManyToManyField(
                    'bb_vm.HostFoundation',
                    through='bb_vm.EquipmentOwner',
                    related_name='owned_equipment'
                )

    def __str__(self):
        return f"{self.account_name } (ID: {self.id})"

    class Meta:
        verbose_name_plural = "Colocation Clients"
        app_label='bb_data'


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
        app_label='bb_data'


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
        app_label='bb_data'

@receiver(post_save, sender=CryptoSnapshot)
def check_new_period_crypto(sender, instance, created, **kwargs):
    '''
    Marks snapshot as starting period if balance is lower than previous entry.
    '''
    print(f"Send by {sender}")
    if created:
        previous_records = CryptoSnapshot.objects.filter(
            account_holder = instance.account_holder).order_by('-id')[:2]

        try:
            if previous_records[0].balance < previous_records[1].balance:
                instance.start_period = True
                instance.save()
        except IndexError:
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
        app_label='bb_data'

@receiver(post_save, sender=FiatSnapshot)
def check_new_period_fiat(sender, instance, created, **kwargs):
    '''
    Marks snapshot as starting period if balance is lower than previous entry.
    '''
    print(f"Send by {sender}")
    if created:
        previous_records = FiatSnapshot.objects.filter(
            account_holder = instance.account_holder).order_by('-id')[:2]

        try:
            if previous_records[0].balance < previous_records[1].balance:
                instance.start_period = True
                instance.save()
        except IndexError:
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
        app_label='bb_data'

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
        app_label='bb_data'


@receiver(post_save, sender=CryptoPayout)
@receiver(post_save, sender=CryptoSnapshot)
def grab_crypto_price(sender, instance, created, **kwargs):
    '''
    On new snapshot, auto adds the value of the crypto.
    '''
    print(f"Send by {sender}")
    if created:

        eth_price = 0
        etherscane_url = 'https://api.etherscan.io/api?module=stats&action=ethprice'

        try:
            eth_result = requests.get(etherscane_url, timeout=5)

            eth = json.loads(eth_result.text)
            eth_price = eth['result']['ethusd']

        except TypeError:
            time.sleep(60)
            eth_result = requests.get(etherscane_url, timeout=5)

            eth = json.loads(eth_result.text)
            eth_price = eth['result']['ethusd']

        except requests.exceptions.SSLError:
            time.sleep(60)
            eth_result = requests.get(etherscane_url, timeout=5)

            eth = json.loads(eth_result.text)
            eth_price = eth['result']['ethusd']

        except json.JSONDecodeError:
            time.sleep(60)
            eth_result = requests.get(etherscane_url, timeout=5)

            eth = json.loads(eth_result.text)
            eth_price = eth['result']['ethusd']


        if sender == CryptoSnapshot:
            instance.dollar_price = float(instance.balance)*float(eth_price)

        if sender == CryptoPayout:
            instance.dollar_price = float(instance.amount)*float(eth_price)

        instance.save()
