'''urls.py for bb_accounts'''

from django.urls import include, path

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
]
