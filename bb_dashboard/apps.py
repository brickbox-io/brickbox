'''apps.py for bb_dashboard'''

from django.apps import AppConfig


class BbDashboardConfig(AppConfig):
    '''
    app specific configuration
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bb_dashboard'
