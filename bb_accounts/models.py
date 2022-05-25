''' bbaccounts | model.py'''

from django.contrib.auth import get_user_model

User = get_user_model()

from bb_data.models import UserProfile

class UserProxy(User):
    ''' Proxy to display users under bb_accounts'''
    class Meta:
        proxy = True
        verbose_name = 'User'
        verbose_name_plural = 'A - Users'

class UserProfileProxy(UserProfile):
    ''' Proxy to display user profiles under bb_accounts'''
    class Meta:
        proxy = True
        verbose_name = 'User Profile'
        verbose_name_plural = 'B - User Profiles'
