'''urls.py for bb_public'''

from django.urls import path

from bb_public import views

app_name = 'bb_public'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),    # Landing/Home Page
    path('legal', views.legal_page, name='legal_page'),   # Legal Page

    # ------------------------------------ PWA ----------------------------------- #
    path('offline/', views.pwa_offline, name='pwa_offline'),    # Offline Page

    # ----------------------------------- Forms ---------------------------------- #
    path('forms/email_list', views.email_list_form, name='email_list_form'),    # Email List Form
    path('forms/contact_us', views.contact_us_form, name='contact_us_form'),    # Contact Us Form
]
