''' Managed SSH keys for users '''

from sshpubkeys import SSHKey as ssh_validator

from sshpubkeys.exceptions import InvalidKeyError

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


from bb_data.models import UserProfile, SSHKey, SSHKeyOwner

@login_required
def add(request):
    '''
    URL: /data/key/add
    Method: POST
    Values: ssh_key, ssh_name
    Used to add a new Public Key for a user.
    '''
    profile = UserProfile.objects.get(user=request.user)

    pub_key = request.POST.get('ssh_key')
    print(pub_key)

    ssh_key = ssh_validator(pub_key)

    try:
        ssh_key.parse()
    except InvalidKeyError:
        return JsonResponse({'saved': False}, status=200, safe=False)

    new_key = SSHKey(name=request.POST['ssh_name'], pub_key=pub_key)
    new_key.save()

    SSHKeyOwner(key=new_key, profile=profile).save()

    return JsonResponse({'saved': True}, status=200, safe=False)
