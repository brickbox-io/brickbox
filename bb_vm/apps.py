''' bb_vm apps.py '''

from django.apps import AppConfig


class BbVmConfig(AppConfig):
    '''
    App specific configuration.
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bb_vm'
    verbose_name: str = "04 | HOSTS & VIRTUAL MACHINES"
