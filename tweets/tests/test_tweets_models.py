from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Tweet

User = get_user_model()


class TestTweetModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@gmail.com',
                                        username='test1',
                                        password='12345')
        self.tweet = Tweet.objects.create(
            user=self.user, content='hello world')

        self.tweet2 = Tweet.objects.create(
            user=self.user,
            content='hello world 2',
            parent=self.tweet)

        self.tweet3 = Tweet.objects.create(
            user=self.user, content='hello world 3')

    def test_tweet_get_parent(self):
        parent = self.tweet.get_parent()
        parent2 = self.tweet2.get_parent()
        self.assertEqual(parent, self.tweet)
        self.assertEqual(parent2, self.tweet)

    def test_get_children(self):
        child = self.tweet.get_children()
        self.assertEqual(child[0], self.tweet2)

    def test_like_toggle(self):
        is_like = Tweet.objects.like_toggle(self.user, self.tweet)
        self.assertTrue(is_like)

    def test_rtweet_func(self):
        retweet = Tweet.objects.retweet(self.user, self.tweet3)
        self.assertTrue(retweet)
        self.assertEqual(retweet.parent, self.tweet3)
        self.assertEqual(retweet.content, self.tweet3.content)
