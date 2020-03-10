from django.test import TestCase, Client
from django.urls import resolve, reverse
from users.views import register, profile, login, logout


class TestUrls(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_url_is_resolved(self):
        url = reverse("register")
        self.assertEquals(resolve(url).func, register)

    def test_profile_url_is_resolved(self):
        url = reverse("profile")
        self.assertEquals(resolve(url).func, profile)