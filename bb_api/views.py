''' views.py for bb_api '''

from django.shortcuts import render

# from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from bb_api.serializers import (
    # UserSerializer, GroupSerializer,
    ColocationClientSerializer, CryptoSnapshotSerializer, FiatSnapshotSerializer,
    CryptoPayoutSerializer, FiatPayoutSerializer, VMLoggingSerializer,
    VirtualBrickSerializer,
)

from bb_data.models import (
        ColocationClient, CryptoSnapshot, FiatSnapshot,
        CryptoPayout, FiatPayout
    )

from bb_vm.models import VMLog, VirtualBrick


def docs(request):
    '''
    Return Slate Docs
    '''
    return render(request, 'api_docs_source/build/index.html')

# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]

class ColocationClientViewSet(viewsets.ModelViewSet):
    '''
    API endpoint for the ColocationClient Model
    '''
    queryset = ColocationClient.objects.all()
    serializer_class = ColocationClientSerializer


class CryptoSnapshotViewSet(viewsets.ModelViewSet):
    '''
    API endpoint to add a crypto holdings amount.
    '''
    queryset = CryptoSnapshot.objects.all()
    serializer_class = CryptoSnapshotSerializer

class FiatSnapshotViewSet(viewsets.ModelViewSet):
    '''
    API endpoing to add fiat holdings amount.
    '''
    queryset = FiatSnapshot.objects.all()
    serializer_class = FiatSnapshotSerializer


class CryptoPayoutViewSet(viewsets.ModelViewSet):
    '''
    API endpoint to record crypto balance payouts to clients.
    '''
    queryset = CryptoPayout.objects.all()
    serializer_class = CryptoPayoutSerializer


class FiatPayoutViewSet(viewsets.ModelViewSet):
    '''
    API endpoint to record fiat balance payouts to clients.
    '''
    queryset = FiatPayout.objects.all()
    serializer_class = FiatPayoutSerializer


# ---------------------------------- Logging --------------------------------- #
class VMLoggingViewSet(viewsets.ModelViewSet):
    '''
    API endpoint to log VM events.
    '''
    queryset = VMLog.objects.all()
    serializer_class = VMLoggingSerializer


# ------------------------------------ VMs ----------------------------------- #
class VirtualBrickViewSet(viewsets.ModelViewSet):
    '''
    API endpoint to manage VM instances.
    '''
    permission_classes = [IsAuthenticated]

    queryset = VirtualBrick.objects.all()
    serializer_class = VirtualBrickSerializer
