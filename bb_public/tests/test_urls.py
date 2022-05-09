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
        # Landing Page
        url_landing_page = reverse('bb_public:landing_page')
        self.assertEqual(url_landing_page, '/')

        # Legal Page
        url_legal_page = reverse('bb_public:legal_page')
        self.assertEqual(url_legal_page, '/legal')

        # Offline Page
        url_offline_page = reverse('bb_public:pwa_offline')
        self.assertEqual(url_offline_page, '/offline/')

        # Email Form
        url_forms_email_list = reverse('bb_public:email_list_form')
        self.assertEqual(url_forms_email_list, '/forms/email_list')

    def test_resolve_urls(self):
        '''
        Test that the correct view is used for the URL request.
        '''
        # Landing Page
        resolve_landing_page = resolve('/')
        self.assertEqual(resolve_landing_page.func.__name__, 'landing_page')
        self.assertEqual(resolve_landing_page.args, ())
        self.assertEqual(resolve_landing_page.kwargs, {})
        self.assertEqual(resolve_landing_page.url_name, 'landing_page')
        self.assertEqual(resolve_landing_page.view_name, 'bb_public:landing_page')

        # Legal Page
        resolve_legal_page = resolve('/legal')
        self.assertEqual(resolve_legal_page.func.__name__, 'legal_page')
        self.assertEqual(resolve_legal_page.args, ())
        self.assertEqual(resolve_legal_page.kwargs, {})
        self.assertEqual(resolve_legal_page.url_name, 'legal_page')
        self.assertEqual(resolve_legal_page.view_name, 'bb_public:legal_page')

        # Offline Page
        resolve_offline_page = resolve('/offline/')
        self.assertEqual(resolve_offline_page.func.__name__, 'pwa_offline')
        self.assertEqual(resolve_offline_page.args, ())
        self.assertEqual(resolve_offline_page.kwargs, {})
        self.assertEqual(resolve_offline_page.url_name, 'pwa_offline')
        self.assertEqual(resolve_offline_page.view_name, 'bb_public:pwa_offline')

        # Email Form
        resolve_email_form = resolve('/forms/email_list')
        self.assertEqual(resolve_email_form.func.__name__, 'email_list_form')
        self.assertEqual(resolve_email_form.args, ())
        self.assertEqual(resolve_email_form.kwargs, {})
        self.assertEqual(resolve_email_form.url_name, 'email_list_form')
        self.assertEqual(resolve_email_form.view_name, 'bb_public:email_list_form')
