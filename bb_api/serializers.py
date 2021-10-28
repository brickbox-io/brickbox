''' serializers.py for bb_api '''

# from django.contrib.auth.models import User, Group
from rest_framework import serializers

from bb_data.models import (
        ColocationClient, CryptoSnapshot, FiatSnapshot,
        CryptoPayout, FiatPayout
    )

from bb_vm.models import VMLog

# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     '''
#     The User Model Serializer
#     '''
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'groups']


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     '''
#     The Group Model Serializer
#     '''
#     class Meta:
#         model = Group
#         fields = ['url', 'name']


class ColocationClientSerializer(serializers.ModelSerializer):
    '''
    Serializer for ColocationClient Model
    '''
    class Meta:
        model = ColocationClient
        fields = ['id', 'account_name']


class CryptoSnapshotSerializer(serializers.ModelSerializer):
    '''
    Serializer for the CryptoSnapshot Model
    '''
    class Meta:
        model = CryptoSnapshot
        fields = ['id', 'recorded', 'account_holder', 'balance', 'currency']
        read_only_fields = ['dollar_price', 'start_period']


class FiatSnapshotSerializer(serializers.ModelSerializer):
    '''
    Serializer for the FiatSnapshot Model
    '''
    class Meta:
        model = FiatSnapshot
        fields = ['id', 'recorded', 'account_holder', 'balance', 'currency']
        read_only_fields = ['start_period']


class CryptoPayoutSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Cryptopayout Model.
    '''
    class Meta:
        model = CryptoPayout
        fields = ['id', 'recorded', 'dated', 'account_holder', 'amount', 'currency', 'tx_hash']
        read_only_fields = ['dollar_price']

class FiatPayoutSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Fiat Model.
    '''
    class Meta:
        model = FiatPayout
        fields = ['id', 'recorded', 'dated', 'account_holder', 'amount', 'currency', 'tx_vast_id']


# ---------------------------------- Logging --------------------------------- #
class VMLoggingSerializer(serializers.ModelSerializer):
    '''
    Serializer for the VMLog Model.
    '''
    class Meta:
        model = VMLog
        fields = [
                    'timestamp', 'level', 'host', 'virt_brick',
                    'message', 'command', 'command_output'
                ]
