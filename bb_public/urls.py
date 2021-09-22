'''urls.py for bb_public'''

from django.urls import path

from bb_public import views

app_name = 'bb_public'

urlpatterns = [
   path('', views.landing_ai, name='ai_landing_page'),
   path('about/', views.about, name='about_page'),
   path('contact/', views.contact, name='contact_page'),
   path('colo/', views.landing_colo, name='colo_landing_page'),

   # ------------------------------------ PWA ----------------------------------- #
   path('offline/', views.pwa_offline, name='pwa_offline'),
]
