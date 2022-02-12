''' admin.py for bb_data '''

from django.contrib import admin

from bb_data.models import (
    UserProfile, ColocationClient, CryptoSnapshot, FiatSnapshot,
    ColocationClientOwner, CryptoPayout, FiatPayout,
    PaymentMethod, PaymentMethodOwner, ResourceRates, ResourceTimeTracking, BillingHistory
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

class CryptoPayoutAdmin(admin.ModelAdmin):
    '''
    Admin configuration for CryptoPayout DB model.
    '''
    list_display = ('dated', 'account_holder', 'amount', 'currency', 'tx_hash', 'dollar_price')

class FiatPayoutAdmin(admin.ModelAdmin):
    '''
    Admin configuration for FiatPayout DB model.
    '''
    list_display = ('dated', 'account_holder', 'amount', 'currency', 'tx_vast_id')

class ResourceRatesAdmin(admin.ModelAdmin):
    '''
    Admin configuration for ResourceRates DB model.
    '''
    list_display = ('resource', 'stripe_price_id',)

class ResourceTimeTrackingAdmin(admin.ModelAdmin):
    '''
    Admin configuration for ResourceTimeTracking DB model.
    '''
    list_display = (
                    'user', 'billing_cycle_start', 'billing_cycle_end',
                    'cycle_total', 'balance_paid',
                    )
    readonly_fields = ('cycle_total',)

class BillingHistoryAdmin(admin.ModelAdmin):
    '''
    Admin configuration for BillingHistory DB model.
    '''
    list_display = ('user', 'date', 'invoice_link', 'invoice_id',)

admin.site.register(UserProfile)
admin.site.register(ColocationClient)
admin.site.register(ColocationClientOwner, ColocationClientOwnerAdmin)
admin.site.register(CryptoSnapshot, CryptoSnapshotAdmin)
admin.site.register(FiatSnapshot, FiatSnapshotAdmin)
admin.site.register(CryptoPayout, CryptoPayoutAdmin)
admin.site.register(FiatPayout, FiatPayoutAdmin)

admin.site.register(PaymentMethod)
admin.site.register(PaymentMethodOwner)
admin.site.register(ResourceRates, ResourceRatesAdmin)
admin.site.register(ResourceTimeTracking, ResourceTimeTrackingAdmin)
admin.site.register(BillingHistory, BillingHistoryAdmin)
