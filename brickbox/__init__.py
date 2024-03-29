'''Ensures the folder can be imported by Python as a package.'''

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from brickbox.brickbox_celery import app as celery_app

__all__ = ["celery_app"]
