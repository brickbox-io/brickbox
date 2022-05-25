''' admin.py for bb_public '''

from django.contrib import admin

from bb_public.models import (
    EmailUpdateList, ContactUs
)

class EmailUpdateListAdmin(admin.ModelAdmin):
    ''' EmailUpdateListAdmin '''
    list_display = ('email', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('email',)

class ContactUsAdmin(admin.ModelAdmin):
    ''' ContactUsAdmin '''
    list_display = ('name', 'email', 'message', 'is_closed')

admin.site.register(EmailUpdateList, EmailUpdateListAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
