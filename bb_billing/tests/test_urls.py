''' bb_billing - test_urls.py '''

from django.test import TestCase
from django.urls import reverse, resolve

class TestUrls(TestCase):
    '''
    Tests performed for each URL:
    - Internal reverse lookup provides the correct URL
    - URL points to the same internal refrence
    - The correct template is served for the URL (if applicable)
    '''

    def test_reverse_urls(self):
        '''
        Reverse lookup tests for each URL
        '''
        # ------------------------- Stripe Webhook Endpoints ------------------------- #
        # Stripe Account
        url_stripe_account = reverse('bb_billing:webhook_stripe_account')
        self.assertEqual(url_stripe_account, '/stripe/account')

        # Stripe Payment Method
        url_stripe_payment_method = reverse('bb_billing:webhook_stripe_pay_method')
        self.assertEqual(url_stripe_payment_method, '/stripe/payment_method')

        # Stripe Invoice
        url_stripe_invoice = reverse('bb_billing:webhook_stripe_invoice')
        self.assertEqual(url_stripe_invoice, '/stripe/invoice')

        # ------------------------- Billing Function Endpoint ------------------------ #
        # Manual Payment
        url_manual_payment = reverse('bb_billing:manual_payment')
        self.assertEqual(url_manual_payment, '/manual_payment')


    def test_resolve_urls(self):
        '''
        Test that the correct view is used for the URL request.
        '''
        # ------------------------- Stripe Webhook Endpoints ------------------------- #
        # Stripe Account
        resolve_stripe_account = resolve('/stripe/account')
        self.assertEqual(resolve_stripe_account.func.__name__, 'account_event')
        self.assertEqual(resolve_stripe_account.args, ())
        self.assertEqual(resolve_stripe_account.kwargs, {})
        self.assertEqual(resolve_stripe_account.url_name, 'webhook_stripe_account')
        self.assertEqual(resolve_stripe_account.view_name, 'bb_billing:webhook_stripe_account')

        # Stripe Payment Method
        resolve_stripe_payment_method = resolve('/stripe/payment_method')
        self.assertEqual(resolve_stripe_payment_method.func.__name__, 'payment_method_event')
        self.assertEqual(resolve_stripe_payment_method.args, ())
        self.assertEqual(resolve_stripe_payment_method.kwargs, {})
        self.assertEqual(resolve_stripe_payment_method.url_name, 'webhook_stripe_pay_method')
        self.assertEqual(resolve_stripe_payment_method.view_name,
                         'bb_billing:webhook_stripe_pay_method')

        #Stripe Invoice
        resolve_stripe_invoice = resolve('/stripe/invoice')
        self.assertEqual(resolve_stripe_invoice.func.__name__, 'invoice_event')
        self.assertEqual(resolve_stripe_invoice.args, ())
        self.assertEqual(resolve_stripe_invoice.kwargs, {})
        self.assertEqual(resolve_stripe_invoice.url_name, 'webhook_stripe_invoice')
        self.assertEqual(resolve_stripe_invoice.view_name, 'bb_billing:webhook_stripe_invoice')

        # ------------------------- Billing Function Endpoint ------------------------ #
        # Manual Payment
        resolve_manual_payment = resolve('/manual_payment')
        self.assertEqual(resolve_manual_payment.func.__name__, 'manual_payment')
        self.assertEqual(resolve_manual_payment.args, ())
        self.assertEqual(resolve_manual_payment.kwargs, {})
        self.assertEqual(resolve_manual_payment.url_name, 'manual_payment')
        self.assertEqual(resolve_manual_payment.view_name, 'bb_billing:manual_payment')
