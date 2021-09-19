''' bb_vm urls.py '''

from django.urls import path

from bb_vm import views, views_validation

app_name = 'bb_vm'

urlpatterns = [
    path('create/', views.clone_img, name='vm_new'),

    path('register/<instance_id>/<domain_uuid>/', views.vm_register, name='vm_register'),
    path('tunnel/', views.vm_tunnel, name='vw_tunnel'),
    path('status/', views.brick_status, name='brick_status'),

    path('error/', views_validation.brick_errors, name='brick_errors'),
    path('state/', views_validation.brick_state, name='brick_state'),

    # ------------------------------- Brick Actions ------------------------------ #
    path('brick/pause/', views.brick_pause, name='brick_pause'),
    path('brick/play/', views.brick_play, name='brick_play'),
    path('brick/reboot/', views.brick_reboot, name='brick_reboot'),
    path('brick/destroy/', views.brick_destroy, name='brick_destroy'),
]
