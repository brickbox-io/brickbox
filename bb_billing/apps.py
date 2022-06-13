''' bb_billing - apps.py '''

from django.apps import AppConfig


class BbBillingConfig(AppConfig):
    '''
    App specific configuration
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bb_billing'
    verbose_name: str = '03 | BILLING'
