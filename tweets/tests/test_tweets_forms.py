from django.test import SimpleTestCase

from ..forms import AddTweetForm


class TestTweetsForms(SimpleTestCase):
    def test_tweets_forms(self):
        form = AddTweetForm(data={'content': 'hello man'})
        self.assertTrue(form.is_valid())
