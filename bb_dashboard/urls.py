'''urls.py for bb_dashboard'''

from django.urls import path, re_path

from bb_dashboard import views

app_name = 'bb_dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Specific Views
    path('<int:colo>', views.dashboard, name='dash_colo'),
    path('colo', views.onboarding, name='colo_onboarding'),

    # ----------------------------------- Tabs ----------------------------------- #
    path('tab/developer/script_add/', views.add_new_script, name='add_new_script'),


    # ------------------- Backwards Compatability Page Handling ------------------ #
    re_path(r'^.*\.*', views.pages, name='pages'),
]
