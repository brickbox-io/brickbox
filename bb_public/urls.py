'''urls.py for bb_public'''

from django.urls import path

from bb_public import views

app_name = 'bb_public'

urlpatterns = [
   path('', views.landing, name='landing_page'),
   path('about/', views.about, name='about_page'),
   path('contact/', views.contact, name='contact_page')
]
