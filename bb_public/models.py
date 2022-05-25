''' bb_public | models.py '''

from django.db import models

# -------------------------- Email Update List Form -------------------------- #
class EmailUpdateList(models.Model):
    '''
    Used to store emails collected from the landing page.
    '''
    email = models.EmailField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ''' Meta class '''
        verbose_name = 'Email Update List'
        verbose_name_plural = 'A - Email List'

# ------------------------------ Contact Us Form ----------------------------- #
class ContactUs(models.Model):
    '''
    Contains messages sent from the contact us form.
    '''
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254)
    message = models.TextField()

    is_closed = models.BooleanField(default=False) # Set to True after message viewed.

    class Meta:
        ''' Meta class '''
        verbose_name = 'Contact Us'
        verbose_name_plural = 'B - Contact Us'
