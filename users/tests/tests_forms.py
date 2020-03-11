from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class TestForms(TestCase):

    @classmethod
    def setUpTest(cls):
        cls.user_1 = User.objects.create_user(
            username="user1",
            password="password@",
            email="user1@user1.com"
        )

    def test_success_creation_form(self):
        data = {
            "username": "user2",
            "password1": "password@",
            "password2": "password@",
            "email": "user2@user2.com",
        }
        form = UserCreationForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        data = {
            "username": "",
            "email": "email@email.fr",
            "password1": "newpassword@",
            "password2": "newpassword@",
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())
    
    def test_password_verification(self):
        data = {
            "username": "user2",
            "password1": "123456@",
            "password2": "123",
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())

    def test_invalid_username(self):
        data = {
            "username": "user3",
            "password": "password@"
        }
        form = AuthenticationForm(None, data)
        self.assertFalse(form.is_valid())

    def test_invalid_password(self):
        data = {
            "username": "user1",
            "password": "12345"
        }
        form = AuthenticationForm(None, data)
        self.assertFalse(form.is_valid())

    """def test_user_already_exists(self):
        data = {
            "username": "user1",
            "email": "email@email.fr",
            "password1": "newpassword@",
            "password2": "newpassword@",
        }
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())
    
    def test_success_authentication(self):
        data = {
            "username": "user1",
            "password": "password@",
        }
        form = AuthenticationForm(None, data)
        self.assertTrue(form.is_valid())"""