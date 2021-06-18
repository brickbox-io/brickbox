from django.contrib import admin
from django.urls import include, path

from bb_dashboard import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]
