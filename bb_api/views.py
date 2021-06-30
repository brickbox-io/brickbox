''' views.py for bb_api '''

from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from rest_framework import permissions

from bb_api.serializers import (
    UserSerializer, GroupSerializer,
    ColocationClientSerializer, CryptoSnapshotSerializer, FiatSnapshotSerializer
)

from bb_data.models import ColocationClient, CryptoSnapshot, FiatSnapshot

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class ColocationClientViewSet(viewsets.ModelViewSet):
    '''
    API endpoint for the ColocationClient Model
    '''
    queryset = ColocationClient.objects.all()
    serializer_class = ColocationClientSerializer
