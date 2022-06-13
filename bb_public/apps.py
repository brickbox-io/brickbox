'''apps.py for bb_public'''

from django.apps import AppConfig


class BbPublicConfig(AppConfig):
    '''
    app specific configurations
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bb_public'
    verbose_name: str = '01 | PUBLIC FORMS'
