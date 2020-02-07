from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import UserProfile

User = get_user_model()


class UserTest(TestCase):
    def setUp(self):
        self.username = 'Masterbdx'
        self.user = User.objects.create(username=self.username)

    def test_user_slug(self):
        username = self.username.lower()
        self.assertIsNotNone(self.user.slug)
        self.assertIn(username, self.user.slug)


class UserProfileTest(TestCase):
    def setUp(self):
        # User 1 -------------------
        self.username = 'Masterbdx'
        self.email = 'masterbdx@gmail.com'
        self.user = User.objects.create(username=self.username,
                                        email=self.email)
        self.profileQs = UserProfile.objects.filter(user=self.user)
        self.profile = self.profileQs.first()

        # User 2 - ------------------
        self.username2 = 'Masterbdx2'
        self.email2 = 'masterbdx2@gmail.com'
        self.user2 = User.objects.create(username=self.username2,
                                         email=self.email2)
        self.profileQs2 = UserProfile.objects.filter(user=self.user2)
        self.profile2 = self.profileQs2.first()

        # User 3 -------------------

        self.username3 = 'Masterbdx3'
        self.email3 = 'masterbdx3@gmail.com'
        self.user3 = User.objects.create(
            username=self.username3,
            email=self.email3)
        self.profileQs3 = UserProfile.objects.filter(
            user=self.user3,
        )
        self.profile3 = self.profileQs3.first()

        # User 4 -------------------

        self.username4 = 'Masterbdx4'
        self.email4 = 'masterbdx4@gmail.com'
        self.user4 = User.objects.create(
            username=self.username4,
            email=self.email4)
        self.profileQs4 = UserProfile.objects.filter(
            user=self.user4,
        )
        self.profile4 = self.profileQs4.first()

        # --------------------
        self.profile.following.add(self.user2, self.user3)

    def test_user_profile_creater(self):
        self.assertTrue(self.profileQs.exists())
        self.assertEqual(self.profile.user.username, self.username)

    def test_profile_get_following_fun(self):

        following = self.profile.get_following()
        self.assertNotIn(self.user, following)
        self.assertEqual(following.count(), 2)

    def test_is_following(self):
        is_follow = UserProfile.objects.is_following(self.user, self.user2)
        self.assertTrue(is_follow)

    def test_recommended_users(self):
        recommended = UserProfile.objects.recommended(self.user)
        self.assertIn(self.profile4, recommended)
        self.assertEqual(self.profile4, recommended.first())

    def test_toggle_user(self):
        toggle = UserProfile.objects.toggle_follow(self.user, self.user4)
        toggle2 = UserProfile.objects.toggle_follow(self.user, self.user4)
        self.assertTrue(toggle)
        self.assertFalse(toggle2)
