''' admin.py for bb_data '''

from django.contrib import admin

from bb_data.models import (
    UserProfile, ColocationClient, CryptoSnapshot, FiatSnapshot,
    ColocationClientOwner, CryptoPayout, FiatPayout
)

class ColocationClientOwnerAdmin(admin.ModelAdmin):
    '''
    Admin configuration for ColocationClientOwner model.
    '''
    list_display = ('owner_profile', 'client_account')

class CryptoSnapshotAdmin(admin.ModelAdmin):
    '''
    Configuration for CryptoSnapshot model DB.
    '''
    list_display = ('recorded', 'account_holder', 'balance', 'currency', 'dollar_price')


class FiatSnapshotAdmin(admin.ModelAdmin):
    '''
    Configuration for FiatSnapshot model DB.
    '''
    list_display = ('recorded', 'account_holder', 'balance', 'currency')

admin.site.register(UserProfile)
admin.site.register(ColocationClient)
admin.site.register(ColocationClientOwner, ColocationClientOwnerAdmin)
admin.site.register(CryptoSnapshot, CryptoSnapshotAdmin)
admin.site.register(FiatSnapshot, FiatSnapshotAdmin)
admin.site.register(CryptoPayout)
admin.site.register(FiatPayout)
