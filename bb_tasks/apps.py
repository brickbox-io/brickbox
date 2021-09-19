''' bb_tasks apps.py '''

from django.apps import AppConfig


class BbTasksConfig(AppConfig):
    '''
    app specific configuration.
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bb_tasks'
