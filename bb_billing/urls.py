'''urls.py for bb_webhook'''

from django.urls import path

from bb_billing import views

app_name = 'bb_webhook'

urlpatterns = [

  # ------------------------- Stripe Webhook Endpoints ------------------------- #
  path('stripe/account', views.account_event, name='webhook_stripe_account'),

  path('stripe/payment_method', views.payment_method_event, name='webhook_stripe_pay_method'),

  path('stripe/invoice', views.invoice_event, name='webhook_invoice_event'),

]
