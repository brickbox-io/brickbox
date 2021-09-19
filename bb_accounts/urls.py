'''urls.py for bb_accounts'''

from django.urls import include, path

from bb_accounts import views

app_name = 'bb_accounts'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.account_registration, name='register'),
]
