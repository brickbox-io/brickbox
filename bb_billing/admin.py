''' bb_billing | admin.py'''

from django.contrib import admin

from bb_billing.models import BillingHistoryProxy

class BillingHistoryProxyAdmin(admin.ModelAdmin):
    ''' Admin site configuration for BillingHistoryProxy '''
    list_display = ['user', 'date', 'invoice_id', 'status']

admin.site.register(BillingHistoryProxy, BillingHistoryProxyAdmin)
