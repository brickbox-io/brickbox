''' bb_accounts - test_urls.py '''

from django.test import TestCase
from django.urls import reverse, resolve

class TestUrls(TestCase):
    '''
    Tests performed for each URL:
    - Internal reverse lookup provides the correct URL
    - URL points to the same internal refrence
    - The correct template is served for the URL (if applicable)
    '''

    def test_reverse_url(self):
        '''
        Reverse lookup tests for each URL
        '''
        # Login URL
        url_login = reverse('bb_accounts:login')
        self.assertEqual(url_login, '/login/')

        # Register URL
        url_login = reverse('bb_accounts:register')
        self.assertEqual(url_login, '/register/')

        # Token URL
        url_login = reverse('bb_accounts:tokensignin')
        self.assertEqual(url_login, '/tokensignin/')

    def test_resolve_urls(self):
        '''
        Test that the correct view is used for the URL request.
        '''
        # Register URL
        resolve_register = resolve('/register/')
        self.assertEqual(resolve_register.func.__name__, 'account_registration')
        self.assertEqual(resolve_register.args, ())
        self.assertEqual(resolve_register.kwargs, {})
        self.assertEqual(resolve_register.url_name, 'register')
        self.assertEqual(resolve_register.view_name, 'bb_accounts:register')

        # Token URL
        resolve_tokensignin = resolve('/tokensignin/')
        self.assertEqual(resolve_tokensignin.func.__name__, 'token_signin')
        self.assertEqual(resolve_tokensignin.args, ())
        self.assertEqual(resolve_tokensignin.kwargs, {})
        self.assertEqual(resolve_tokensignin.url_name, 'tokensignin')
        self.assertEqual(resolve_tokensignin.view_name, 'bb_accounts:tokensignin')
