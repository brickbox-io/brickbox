from django.contrib import admin

from bb_accounts.models import UserProxy, UserProfileProxy

class UserProxyAdmin(admin.ModelAdmin):
    '''
    Admin configuration for the UserProxy model.
    '''
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'last_login', )

class UserProfileProxyAdmin(admin.ModelAdmin):
    '''
    Admin configuration for the User Profile model.
    '''
    list_display = ('user', 'brick_access')

admin.site.register(UserProxy, UserProxyAdmin)
admin.site.register(UserProfileProxy, UserProfileProxyAdmin)
