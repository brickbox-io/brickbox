''' bb_vm urls.py '''

from django.urls import path

from bb_vm import views, views_validation, views_host

app_name = 'bb_vm'

urlpatterns = [
    # ------------------------------- Host Actions ------------------------------- #
    path(
            'host/onboarding/<host_serial>/',
            views_host.onboarding,
            name='host_onboarding'
        ),
    path(
            'host/onboarding/pubkey/<host_serial>/',
            views_host.onboarding_pubkey,
            name='host_onboarding_pubkey'
        ),
    path(
            'host/onboarding/sshport/<host_serial>/',
            views_host.onboarding_sshport,
            name='host_onboarding_ssh'
        ),
    path(
            'host/onboarding/gpu/<host_serial>/',
            views_host.onboarding_gpu,
            name='host_onboarding_gpu'
        ),
    path(
            'host/garbage/<host_serial>/',
            views_host.garbage_collection,
            name='host_garbage_collection'
        ),

    # -------------------------------- VM Creation ------------------------------- #
    path('create/', views.clone_img, name='vm_new'),

    path('register/<instance_id>/<domain_uuid>/', views.vm_register, name='vm_register'),

    path('tunnel/', views.vm_tunnel, name='vw_tunnel'),

    path('status/', views.brick_status, name='brick_status'),

    path('error/', views_validation.brick_errors, name='brick_errors'),


    # ------------------------------- Brick Actions ------------------------------ #
    path('brick/pause/', views.brick_pause, name='brick_pause'),        # Shutdown VM

    path('brick/play/', views.brick_play, name='brick_play'),           # Start VM

    path('brick/reboot/', views.brick_reboot, name='brick_reboot'),     # Reboot VM

    path('brick/destroy/', views.brick_destroy, name='brick_destroy'),  # Destroy VM

    # -------------------------------- Brick Info -------------------------------- #
    path('brick/info', views.brick_info, name='brick_info'),

    path('brick/update_resources', views.update_brick_resources, name='update_brick_resources'),
]
