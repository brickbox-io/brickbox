'''urls.py for bb_data'''

from django.urls import path

from bb_data import views_charts

app_name = 'bb_data'

urlpatterns = [
   path('cryptochart/', views_charts.crypto_balance_chart, name='crypto_chart'),
   path('cryptochart/<int:colo>', views_charts.crypto_balance_chart, name='crypto_chart_colo'),

   path('fiatchart/', views_charts.fiat_balance_chart, name='fiat_chart'),
   path('fiatchart/<int:colo>', views_charts.fiat_balance_chart, name='fiat_chart_colo'),

   path('monthlybreakdown/', views_charts.monthly_breakdown_chart, name='monthly_breakdown'),
]
