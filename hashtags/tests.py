from django.contrib.auth import get_user_model
from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve

from .models import Hashtag
from tweets.models import Tweet
from .views import HashtagView


User = get_user_model()


class TestHashModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='m@gmail.com',
                                        username='hello',
                                        password='12345')
        self.tweet = Tweet.objects.create(user=self.user,
                                          content='hello #omar')
        self.hashtag = Hashtag.objects.create(tag='omar')

    def test_hash_get_tweets_func(self):
        tweets = self.hashtag.get_tweets()
        self.assertEqual(tweets.first(), self.tweet)


class TestHashTagsView(TestCase):
    def setUp(self):
        self.client = Client()
        self.hashtag = Hashtag.objects.create(tag='omar')

    def test_hashtag_view(self):
        url = reverse('hashtags:name', kwargs={'hashtag': self.hashtag})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hashtags/hashtag.html')


class TestHashTagsUrls(SimpleTestCase):
    def test_hashtag_url(self):
        url = reverse('hashtags:name', kwargs={'hashtag': 'omar'})
        url_resolved = resolve(url)
        self.assertEqual(url_resolved.func.view_class, HashtagView)
