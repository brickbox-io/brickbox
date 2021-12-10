'''urls.py for bb_webhook'''

from django.urls import path

from bb_webhook import views_stripe

app_name = 'bb_webhook'

urlpatterns = [
  # ------------------------- Stripe Webhook Endpoints ------------------------- #
  path('stripe/account', views_stripe.account_event, name='webhook_stripe_account'),
  path('stripe/payment_method', views_stripe.payment_method_event, name='webhook_stripe_payment_method'),
]
