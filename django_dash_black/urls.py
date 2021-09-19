# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from django_dash_black import views

app_name = 'django_dash_black'

urlpatterns = [

    # The home page
    path('', views.index, name='dash'),
    path('<int:colo>', views.index, name='dash_colo'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
