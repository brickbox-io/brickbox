''' apps.py for bb_api '''

from django.apps import AppConfig


class BbApiConfig(AppConfig):
    '''
    app specific configuration
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bb_api'
