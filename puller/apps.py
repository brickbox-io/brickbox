''' puller apps.py '''

from django.apps import AppConfig


class PullerConfig(AppConfig):
    '''
    App specific configurations.
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'puller'
