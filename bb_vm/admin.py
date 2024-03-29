''' bb_vm admin view model registration page '''

from django.contrib import admin

from bb_vm.models import(
    PortTunnel, VirtualBrick, VirtualBrickHistory, VirtualBrickOwner,
    GPU, HostFoundation, EquipmentOwner, RentedGPU, VMLog,

    # Models Config
    CloudImage, BackgroundTask
)


# ---------------------------------------------------------------------------- #
#                             Admin Configurations                             #
# ---------------------------------------------------------------------------- #


class PortTunnelAdmin(admin.ModelAdmin):
    ''' PortTunnel admin view model registration '''
    list_display = ('port_number', 'is_alive')
    list_filter = ('is_alive',)
    search_fields = ('port_number', 'poris_alivet')
    ordering = ('port_number',)

class HostFoundationAdmin(admin.ModelAdmin):
    '''
    Admin configuration for HostFoundation model.
    '''
    list_display = ('vpn_ip', 'ssh_port', 'is_enabled', 'is_online', 'is_ready')
    readonly_fields = ['ssh_port', 'sshtunnel_public_key', 'ssh_username', 'is_online', 'is_ready']

class GPUAdmin(admin.ModelAdmin):
    '''
    Admin configuration for GPU model.
    '''
    list_display = (
                        'id', 'host', 'model', 'pcie', 'device',
                        'is_enabled', 'rented', 'attached_to',
                        'bg_ready', 'bg_running'
                    )
    readonly_fields = ('rented', 'attached_to', 'bg_ready', 'bg_running')

class RentedGPUAdmin(admin.ModelAdmin):
    '''
    Admin configuration for RentedGPU model.
    '''
    list_display = ('gpu', 'virt_brick')

class VirtualBrickAdmin(admin.ModelAdmin):
    '''
    Admin configuration for VirtualBrick model.
    '''
    list_display = ('id', 'domain_uuid', 'host', 'ssh_port', 'img_cloned', 'is_rebooting', 'is_on')
    readonly_fields = ('img_cloned', 'is_rebooting', 'is_on')

class VirtualBrickHistoryAdmin(admin.ModelAdmin):
    '''
    Admin configuration for VirtualBrickHistory model.
    '''
    list_display = ('brick', 'creator')

class VirtualBrickOwnerAdmin(admin.ModelAdmin):
    '''
    Admin configuration for VirtualBrickOwner model.
    '''
    list_display = ('owner', 'virt_brick')

class VMLogAdmin(admin.ModelAdmin):
    '''
    Admin configuration for VMLog model.
    '''
    list_display = ('timestamp', 'level', 'command', 'virt_brick')
    readonly_fields = (
                        'timestamp', 'level', 'host', 'virt_brick',
                       'message', 'command', 'command_output'
                      )
    search_fields = ('virt_brick',)
    list_filter = ('host', 'level',)

# ------------------------------- Models Config ------------------------------ #
class CloudImageAdmin(admin.ModelAdmin):
    '''
    Admin configuration for CloudImage model.
    '''
    list_display = ('distribution', 'version', 'is_active')

class BackgroundTaskAdmin(admin.ModelAdmin):
    '''
    Admin configuration for BackgroundTask model.
    '''
    list_display = ('id', 'name', 'description',)

# ---------------------------------------------------------------------------- #
#                              Admin Registrations                             #
# ---------------------------------------------------------------------------- #


admin.site.register(PortTunnel, PortTunnelAdmin)
admin.site.register(HostFoundation, HostFoundationAdmin)
admin.site.register(EquipmentOwner)
admin.site.register(GPU, GPUAdmin)
admin.site.register(RentedGPU, RentedGPUAdmin)
admin.site.register(VirtualBrick, VirtualBrickAdmin)
admin.site.register(VirtualBrickHistory, VirtualBrickHistoryAdmin)
admin.site.register(VirtualBrickOwner, VirtualBrickOwnerAdmin)
admin.site.register(VMLog, VMLogAdmin)

# ------------------------------- Models Config ------------------------------ #
admin.site.register(CloudImage, CloudImageAdmin)
admin.site.register(BackgroundTask, BackgroundTaskAdmin)
