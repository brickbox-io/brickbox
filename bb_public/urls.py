'''urls.py for bb_public'''

from django.urls import path

from bb_public import views

app_name = 'bb_public'

urlpatterns = [
    path('', views.landing, name='landing_page'),    # Landing/Home Page
    path('legal', views.legal, name='legal_page'),   # Legal Page

    # ------------------------------------ PWA ----------------------------------- #
    path('offline/', views.pwa_offline, name='pwa_offline'),    # Offline Page

    # ----------------------------------- Forms ---------------------------------- #
    path('forms/email_list', views.forms_email_list, name='forms_email_list'),
]
