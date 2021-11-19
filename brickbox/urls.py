"""brickbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls import url


# --------------------------- Admin Customizations --------------------------- #
admin.site.site_header = "brickbox.io"
admin.site.site_title = "brickbox.io"
admin.site.index_title = "Admin Interface"

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('bb_api.urls')),               # bb_api
    path('', include('bb_accounts.urls')),              # bb_accounts
    path('', include('bb_public.urls')),                # bb_public
    path('dashboard/', include('bb_dashboard.urls')),   # bb_dashboard
    path('dash/', include('django_dash_black.urls')),
    path('data/', include('bb_data.urls')),             # bb_data
    path('webhook/', include('bb_webhook.urls')),       # bb_webhook

    # ---------------------------- Virtulization URLS ---------------------------- #
    path('vm/', include('bb_vm.urls')),                 # bb_vm

    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')), # OAuth2.0
    # path('api-auth/', include('rest_framework.urls')),

    path('accounts/', include('allauth.urls')),     # django-allauth

    path('puller/', include('puller.urls')),        # Puller App

    path('status/', include('health_check.urls')),  # django-health-check

    url('', include('pwa.urls')),                   # Progressive Web App (PWA)
]
