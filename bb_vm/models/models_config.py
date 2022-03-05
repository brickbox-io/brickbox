''' bb_vm - models_config.py '''

from django.db import models


# -------------------------------- Cloud Image ------------------------------- #
class CloudImage(models.Model):
    '''
    Defines the cloud images that are able to be selected by a user.
    '''
    distribution = models.CharField(max_length=100)
    version = models.CharField(max_length=100)

    img_url = models.CharField(max_length=200)
    checksum_url = models.CharField(max_length=200)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.distribution} - {self.version}"

    class Meta:
        verbose_name_plural = "Cloud Images"
