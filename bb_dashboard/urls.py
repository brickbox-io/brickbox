'''urls.py for bb_dashboard'''

from django.urls import include, path

from bb_dashboard import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]
