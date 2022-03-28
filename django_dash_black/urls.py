# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from django_dash_black import views, views_colo

app_name = 'django_dash_black'

urlpatterns = [

    # The home page
    path('', views.index, name='dash'),
    path('<int:colo>', views.index, name='dash_colo'),

    # Specific Views
    path('colo', views_colo.onboarding, name='colo_onboarding'),

]
