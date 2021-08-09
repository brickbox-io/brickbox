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
    url('', include('pwa.urls')),  # Progressive Web App (PWA)
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('bb_api.urls')),
    path('', include('bb_accounts.urls')),
    path('', include('bb_public.urls')),
    path('dashboard/', include('bb_dashboard.urls')),
    path('dash/', include('django_dash_black.urls')),
    path('data/', include('bb_data.urls')),
    # path('api-auth/', include('rest_framework.urls'))
]
