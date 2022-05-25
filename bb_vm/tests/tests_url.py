''' bb_vm | tests.url.py '''

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
        Reverse lookup tests for each URL.
        '''
        # Host Onboard
        url_host_onboard = reverse('bb_vm:host_onboarding', kwargs={'host_serial': '1234567890'})
        self.assertEqual(url_host_onboard, 'vm/host/oboarding/')
