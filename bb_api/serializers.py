''' serializers.py for bb_api '''

# from django.contrib.auth.models import User, Group
from rest_framework import serializers

from bb_data.models import ColocationClient, CryptoSnapshot, FiatSnapshot

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
        fields = ['id', 'recorded', 'account_holder', 'balance', 'currency', 'dollar_price',]
        read_only_fields = ['dollar_price',]


class FiatSnapshotSerializer(serializers.ModelSerializer):
    '''
    Serializer for the FiatSnapshot Model
    '''
    class Meta:
        model = FiatSnapshot
        fields = ['id', 'recorded', 'account_holder', 'balance', 'currency']
