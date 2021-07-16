'''urls.py for bb_data'''

from django.urls import path

from bb_data import views_charts

urlpatterns = [
   path('cryptochart/', views_charts.crypto_balance_chart, name='crypto_chart'),
   path('fiatchart/', views_charts.fiat_balance_chart, name='fiat_chart'),
]
