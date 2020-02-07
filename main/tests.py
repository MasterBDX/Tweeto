from django.test import TestCase, Client
from django.urls import reverse


class TestMainViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_serach_view(self):
        url = reverse('search')
        response = self.client.get(url, data={'q': 'hello'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/results.html')
