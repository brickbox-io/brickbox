'''urls.py for bb_accounts'''

from django.urls import include, path

app_name = 'bb_accounts'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
]
