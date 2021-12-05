''' bb_colo - views.py '''

from django.shortcuts import render
from django.http import HttpResponse

from bb_data.models import UserProfile, ColocationClient, ColocationClientOwner

def agreement(request):
    '''
    URL: /colo/agreement
    '''
    print(request.POST)
    profile = UserProfile.objects.get(user=request.user)
    clients = ColocationClientOwner.objects.filter(owner_profile=profile)

    print(clients)

    client = clients[0].client_account

    print(client)

    client.term_agreement = True
    client.save()

    return HttpResponse(status=200)
