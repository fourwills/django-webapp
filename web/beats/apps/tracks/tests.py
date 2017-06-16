from django.core.urlresolvers import reverse
from django.test import Client, TestCase


class IndexTestCase(TestCase):
    """ Test Index Template exists """
    def setUp(self):
        self.client = Client()

    def test_should_always_pass(self):
        self.assertEqual(1, 1)

    def test_can_access_index_page_successfully(self):
        response = self.client.get(reverse('tracks:index'))
        self.assertEqual(response.status_code, 200)
