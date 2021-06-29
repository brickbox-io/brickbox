''' admin.py for bb_data '''

from django.contrib import admin

from bb_data.models import ColocationClient, CryptoSnapshot, FiatSnapshot

admin.site.register(ColocationClient)
admin.site.register(CryptoSnapshot)
admin.site.register(FiatSnapshot)
