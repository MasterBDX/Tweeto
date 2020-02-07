from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from tweets.models import Tweet
from ..models import UserProfile
User = get_user_model()


class TestAccountsViews(TestCase):
    def setUp(self):
        self.username = 'masterbdx'
        self.email = 'masterbdx@gmail.com'
        self.password = '123456789'
        self.user = User.objects.create_superuser(email=self.email,
                                                  username=self.username,
                                                  password=self.password,
                                                  subscribed=True
                                                  )

        self.tweet = Tweet.objects.create(
            user=self.user,
            content='hello world',)

        self.client = Client()

    def test_login_view(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_logout_view(self):
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)

    def test_profile_view(self):
        url = reverse('accounts:profile', kwargs={'user_slug': self.user.slug})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        url = reverse('accounts:register')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertEqual(response.status_code, 200)

    def test_userfollow_view(self):
        url = reverse('accounts:follow', kwargs={'user_slug': self.user.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(
            email=self.email, password=self.password)
        self.assertEqual(response.status_code, 302)

    def test_follow_manager_view(self):
        url = reverse('accounts:follow_manage', kwargs={
                      'user_slug': self.user.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(
            email=self.email, password=self.password)
        self.assertEqual(response.status_code, 302)

    def test_profile_update_view(self):
        url = reverse('accounts:profile_update', kwargs={
                      'pk': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_followers_view(self):
        url = reverse('accounts:followers', kwargs={
                      'user_slug': self.user.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/followers.html')

    def test_following_view(self):
        url = reverse('accounts:following', kwargs={
                      'user_slug': self.user.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/following.html')

    def test_user_like_view(self):
        url = reverse('accounts:user-like', kwargs={
                      'slug': self.user.slug, 'pk': self.tweet.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.login(
            email=self.email, password=self.password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_theme_view(self):
        url = reverse('accounts:theme')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(
            email=self.email, password=self.password)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
