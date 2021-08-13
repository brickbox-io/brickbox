''' bb_vm admin view model registration page '''

from django.contrib import admin

from bb_vm.models import(
     VirtualBrick, PortTunnel, VirtualBrickOwner,
     GPU, HostFoundation, RentedGPU
)

admin.site.register(VirtualBrick)
admin.site.register(PortTunnel)
admin.site.register(VirtualBrickOwner)
admin.site.register(GPU)
admin.site.register(HostFoundation)
admin.site.register(RentedGPU)
