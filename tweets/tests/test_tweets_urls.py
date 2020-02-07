from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.views.generic.base import RedirectView

from ..views import (TweetListView,
                     TweetDetailView,
                     TweetCreateView,
                     TweetEditView,
                     TweetDeleteView,
                     RetweetView)


class TestTweetsUrls(SimpleTestCase):
    def test_redirect_url(self):
        url = '/tweets/'
        self.assertEqual(resolve(url).func.view_class, RedirectView)

    def test_tweets_list_view(self):
        url = reverse('tweets:list')
        self.assertEqual(resolve(url).func.view_class, TweetListView)

    def test_tweets_detail_view(self):
        url = reverse('tweets:detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, TweetDetailView)

    def test_tweets_retweet_view(self):
        url = reverse('tweets:retweet', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, RetweetView)

    def test_tweets_edit_view(self):
        url = reverse('tweets:edit', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, TweetEditView)

    def test_tweets_delete_view(self):
        url = reverse('tweets:delete', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, TweetDeleteView)
