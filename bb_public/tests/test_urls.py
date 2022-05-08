''' bb_public - test_urls.py '''

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
        url_landing_page = reverse('bb_public:landing_page')
        self.assertEqual(url_landing_page, '/')

        url_legal_page = reverse('bb_public:legal_page')
        self.assertEqual(url_legal_page, '/legal')

        url_offline_page = reverse('bb_public:pwa_offline')
        self.assertEqual(url_offline_page, '/offline/')

        url_forms_email_list = reverse('bb_public:forms_email_list')
        self.assertEqual(url_forms_email_list, '/forms/email_list')

    def test_resolver_urls(self):
        '''
        Test that the correct view is used for the URL request.
        '''
        resolver_landing_page = resolve('/')
        self.assertEqual(resolver_landing_page.func.__name__, 'landing_page')
        self.assertEqual(resolver_landing_page.args, ())
        self.assertEqual(resolver_landing_page.kwargs, ())
        self.assertEqual(resolver_landing_page.url_name, '/')
        self.assertEqual(resolver_landing_page.view_name, 'bb_public:landing_page')
