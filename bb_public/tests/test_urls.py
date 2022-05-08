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
        self.assertEqual(url_legal_page, '/legal/')
