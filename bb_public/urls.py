from django.contrib import admin
from django.urls import path, include

from bb_public import views

urlpatterns = [
   path('', views.landing, name='landing_page'),
   path('about/', views.about, name='about_page'),
   path('contact/', views.contact, name='contact_page')
]
