''' apps.py for bb_accounts '''

from django.apps import AppConfig


class BbAccountsConfig(AppConfig):
    '''
    app specific configurations
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bb_accounts'
    verbose_name = "02 | ACCOUNTS"
