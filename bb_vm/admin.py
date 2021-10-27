''' bb_vm admin view model registration page '''

from django.contrib import admin

from bb_vm.models import(
     VirtualBrick, PortTunnel, VirtualBrickOwner,
     GPU, HostFoundation, RentedGPU, VMLog
)

class HostFoundationAdmin(admin.ModelAdmin):
    '''
    Admin configuration for HostFoundation model.
    '''
    list_display = ('ssh_port', 'active', 'connected_status', 'is_online', 'gpus_online')

class GPUAdmin(admin.ModelAdmin):
    '''
    Admin configuration for GPU model.
    '''
    list_display = ('id', 'host', 'model', 'pcie', 'device', 'rented')

class RentedGPUAdmin(admin.ModelAdmin):
    '''
    Admin configuration for RentedGPU model.
    '''
    list_display = ('gpu', 'virt_brick')

class VirtualBrickAdmin(admin.ModelAdmin):
    '''
    Admin configuration for VirtualBrick model.
    '''
    list_display = ('id', 'domain_uuid', 'ssh_port', 'img_cloned', 'is_rebooting', 'is_on')

class VirtualBrickOwnerAdmin(admin.ModelAdmin):
    '''
    Admin configuration for VirtualBrickOwner model.
    '''
    list_display = ('owner', 'virt_brick')

class VMLogAdmin(admin.ModelAdmin):
    '''
    Admin configuration for VMLog model.
    '''
    list_display = ('timestamp', 'level', 'virt_brick')

admin.site.register(PortTunnel)
admin.site.register(HostFoundation, HostFoundationAdmin)
admin.site.register(GPU, GPUAdmin)
admin.site.register(RentedGPU, RentedGPUAdmin)
admin.site.register(VirtualBrick, VirtualBrickAdmin)
admin.site.register(VirtualBrickOwner, VirtualBrickOwnerAdmin)
admin.site.register(VMLog, VMLogAdmin)
