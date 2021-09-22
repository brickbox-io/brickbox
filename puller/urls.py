''' puller urls.py '''

from django.urls import path

from puller import views

urlpatterns = [
    path('cd/', views.pull_update, name='CD'),
]
