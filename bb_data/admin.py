''' admin.py for bb_data '''

from django.contrib import admin

from bb_data.models import (
    UserProfile, ColocationClient, CryptoSnapshot, FiatSnapshot,
    ColocationClientOwner
)

class CryptoSnapshotAdmin(admin.ModelAdmin):
    '''
    Configuration for CryptoSnapshot model DB.
    '''
    list_display = ('recorded', 'account_holder', 'balance', 'currency', 'dollar_price')


admin.site.register(UserProfile)
admin.site.register(ColocationClient)
admin.site.register(ColocationClientOwner)
admin.site.register(CryptoSnapshot, CryptoSnapshotAdmin)
admin.site.register(FiatSnapshot)
