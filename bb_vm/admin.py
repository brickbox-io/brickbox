''' bb_vm admin view model registration page '''

from django.contrib import admin

from bb_vm.models import(
     VirtualBrick, PortTunnel, VirtualBrickOwner,
     GPU, HostFoundation, RentedGPU
)

class HostFoundationAdmin(admin.ModelAdmin):
    list_display = ('ssh_port', 'active', 'connected_status')

class GPUAdmin(admin.ModelAdmin):
    list_display = ('id', 'host', 'model', 'pcie', 'device', 'rented')

class RentedGPUAdmin(admin.ModelAdmin):
    list_display = ('gpu', 'virt_brick')

class VirtualBrickAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain_uuid', 'ssh_port', 'img_cloned', 'is_rebooting', 'is_on')

class VirtualBrickOwnerAdmin(admin.ModelAdmin):
    list_display = ('owner', 'virt_brick')

admin.site.register(PortTunnel)
admin.site.register(HostFoundation, HostFoundationAdmin)
admin.site.register(GPU, GPUAdmin)
admin.site.register(RentedGPU, RentedGPUAdmin)
admin.site.register(VirtualBrick, VirtualBrickAdmin)
admin.site.register(VirtualBrickOwner, VirtualBrickOwnerAdmin)
