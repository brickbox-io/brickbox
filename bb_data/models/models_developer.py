''' bb_data - models_developer.py '''

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomScript(models.Model):
    '''
    Defines scripts that a user can create to run when launching a brick.
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    script = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
