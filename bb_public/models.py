''' models.py for bb_public '''

from django.db import models

class EmailUpdateList(models.Model):
    '''
    EmailUpdateList model
    Used to store emails collected from the landing page.
    '''
    email = models.EmailField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ''' Meta class '''
        verbose_name = 'Email Update List'
        verbose_name_plural = 'Email List'
