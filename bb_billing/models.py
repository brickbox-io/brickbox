''' bb_billing | models.py '''

from tabnanny import verbose
from bb_data.models import BillingHistory

class BillingHistoryProxy(BillingHistory):
    ''' BillingHistoryProxy '''
    class Meta:
        proxy = True
        verbose_name = 'Billing History'
        verbose_name_plural = 'A - Billing History'
