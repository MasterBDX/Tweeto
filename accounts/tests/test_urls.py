from django.test import SimpleTestCase
from django.urls import reverse, resolve

from ..views import (UserLoginView, UserRegistrerView, UserProfileUpdateView,
                     UserLogoutView, UserProfileView, UserFollow, ThemeChange,
                     FollowManager, FollowingView, FollowersView)
from tweets.api.views import ProfileLikeToggleApiView


class TestAccountsUrls(SimpleTestCase):
    def test_login(self):
        url = reverse('accounts:login')
        self.assertEqual(resolve(url).func.view_class, UserLoginView)

    def test_logout(self):
        url = reverse('accounts:logout')
        self.assertEqual(resolve(url).func.view_class, UserLogoutView)

    def test_register(self):
        url = reverse('accounts:register')
        self.assertEqual(resolve(url).func.view_class, UserRegistrerView)

    def test_follow(self):
        url = reverse('accounts:follow', kwargs={'user_slug': 'masterbdx'})
        self.assertEqual(resolve(url).func.view_class, UserFollow)

    def test_follow_manage(self):
        url = reverse('accounts:follow_manage', kwargs={
                      'user_slug': 'masterbdx'})
        self.assertEqual(resolve(url).func.view_class, FollowManager)

    def test_profile(self):
        url = reverse('accounts:profile', kwargs={
                      'user_slug': 'masterbdx'})
        self.assertEqual(resolve(url).func.view_class, UserProfileView)

    def test_profile_edit(self):
        url = reverse('accounts:profile_update', kwargs={
                      'pk': 1})
        self.assertEqual(resolve(url).func.view_class, UserProfileUpdateView)

    def test_followers(self):
        url = reverse('accounts:followers', kwargs={
                      'user_slug': 'masterbdx'})
        self.assertEqual(resolve(url).func.view_class, FollowersView)

    def test_following(self):
        url = reverse('accounts:following', kwargs={
                      'user_slug': 'masterbdx'})
        self.assertEqual(resolve(url).func.view_class, FollowingView)

    def test_user_like(self):
        url = reverse('accounts:user-like', kwargs={
                      'pk': 1, 'slug': 'masterbdx'})
        self.assertEqual(resolve(url).func.view_class,
                         ProfileLikeToggleApiView)

    def test_theme(self):
        url = reverse('accounts:theme')
        self.assertEqual(resolve(url).func.view_class,
                         ThemeChange)
