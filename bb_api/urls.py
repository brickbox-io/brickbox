''' urls.py for bb_api '''

from django.urls import include, path
from rest_framework import routers

from bb_api import views

aap_name = 'bb_api'

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
router.register(r'clients', views.ColocationClientViewSet)
router.register(r'cryptosnapshot', views.CryptoSnapshotViewSet)
router.register(r'fiatsnapshot', views.FiatSnapshotViewSet)
router.register(r'cryptopayout', views.CryptoPayoutViewSet)
router.register(r'fiatpayout', views.FiatPayoutViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
