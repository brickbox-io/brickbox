''' apps.py for bb_data '''

from django.apps import AppConfig


class BbDataConfig(AppConfig):
    '''
    app specific configurations
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bb_data'
