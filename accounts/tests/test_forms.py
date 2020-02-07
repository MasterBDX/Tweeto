from django.test import SimpleTestCase, TestCase

from ..forms import (LoginForm, RegistrationForm, UserProfileColorForm)


class TestAccountsForms(TestCase):

    def test_registration_form(self):
        form = RegistrationForm(data={'username': 'test',
                                      'email': 'test@gmail.com',
                                      'password': '12345',
                                      'password2': '12345'})
        self.assertTrue(form.is_valid())

    def test_user_profile_color_code(self):
        form = UserProfileColorForm(data={'color': ' #ccd1d1 '})
        self.assertTrue(form.is_valid())
        form = UserProfileColorForm(data={'color': ' #ccd1d1 ::'})
        self.assertFalse(form.is_valid())
