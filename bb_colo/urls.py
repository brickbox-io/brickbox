''' bb_colo urls.py '''

from django.urls import include, path

from bb_colo import views

urlpatterns = [
    path('agreement/', views.agreement, name='colo_agreement'),
]
