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
        self.assertEqual(url_host_onboard, '/vm/host/onboarding/1234567890/')

        # Host Onboard Public Key
        url_host_onboard_pubkey = reverse(
                                        'bb_vm:host_onboarding_pubkey',
                                        kwargs={'host_serial': '1234567890'}
                                    )
        self.assertEqual(url_host_onboard_pubkey, '/vm/host/onboarding/pubkey/1234567890/')

        # Host Onboard SSH Port
        url_host_onboard_sshport = reverse(
                                        'bb_vm:host_onboarding_ssh',
                                        kwargs={'host_serial': '1234567890'}
                                    )
        self.assertEqual(url_host_onboard_sshport, '/vm/host/onboarding/sshport/1234567890/')

    def test_resolve_urls(self):
        '''
        Test that the correct view is used for the URL request.
        '''
        # Host Onboard
        resolve_host_onboard = resolve('/vm/host/onboarding/1234567890/')
        self.assertEqual(resolve_host_onboard.func.__name__, 'onboarding')
        self.assertEqual(resolve_host_onboard.args, ())
        self.assertEqual(resolve_host_onboard.kwargs['host_serial'], '1234567890')
        self.assertEqual(resolve_host_onboard.url_name, 'host_onboarding')
        self.assertEqual(resolve_host_onboard.view_name, 'bb_vm:host_onboarding')

        # Host Onboard Public Key
        resolve_host_onboard_pubkey = resolve('/vm/host/onboarding/pubkey/1234567890/')
        self.assertEqual(resolve_host_onboard_pubkey.func.__name__, 'onboarding_pubkey')
        self.assertEqual(resolve_host_onboard_pubkey.args, ())
        self.assertEqual(resolve_host_onboard_pubkey.kwargs['host_serial'], '1234567890')
        self.assertEqual(resolve_host_onboard_pubkey.url_name, 'host_onboarding_pubkey')
        self.assertEqual(resolve_host_onboard_pubkey.view_name, 'bb_vm:host_onboarding_pubkey')
